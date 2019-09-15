from django.conf import settings
from datetime import datetime, date, timedelta
import time
from django.db import models
import jwt
from django.utils import timezone
from django.core.validators import EmailValidator, MinLengthValidator
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.auth import password_validation
STATUS = settings.STATUS
log = settings.LOG
# Create your models here.


class UserManager(BaseUserManager):

 # how serializer diff than create user  and  paramaetre of create user ??
    def create_user(self, email, name, mobile, dob, token_type, password, roleid=1,):
        log.info("create_user function has been called")
        user = self.model(email=self.normalize_email(email),
                          name=name, mobile=mobile, dob=dob, roleid=roleid)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

    userid = models.AutoField(primary_key=True, default=None)
    email = models.EmailField(unique=True, validators=[EmailValidator])
    password = models.CharField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=12, validators=[
        MinLengthValidator(5)])
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    dob = models.DateField(default=date.today)
    roleid = models.IntegerField(default=1)
    userstatus = models.IntegerField(default=1)
    token_type = models.IntegerField(default=1)
    is_staff = models.BooleanField(default=False)
# manadatory for django USermodel
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return "%s (%s,%s,%s,%s,%s)" % (self.userid, self.name, self.mobile, self.dob, self.email, self.modified_on)

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):

        log.info("token generating")
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        if self.token_type in (STATUS.ACCESS_TOKEN_CONFIRMATION, STATUS.ACCESS_TOKEN_FORGOT_PASSWORD):
            dt = datetime.utcnow() + timedelta(days=1)
        else:
            dt = datetime.utcnow() + timedelta(days=20)
        token = jwt.encode({
            'id': self.userid,
            'exp': dt,
            'token_type': self.token_type,
        }, settings.SECRET_KEY, algorithm='HS256')
        log.info("token generated %s", token)

        return token.decode('utf-8')

    class Meta:
        ordering = ['-created_on']


class UserRoles(models.Model):
    roleid = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=15)

    def __str__(self):
        return "%s" % (self.roleid)
