# from django.conf import settings
# from rest_framework import serializers
# from authentication.models import User
# from django.contrib.auth import authenticate

# log = settings.LOG


# class SignupSerializer(serializers.ModelSerializer):

#     log.info("Signup serializer settings")

#     # doubt :  Token serialize >?
#     token = serializers.CharField(max_length=255, read_only=True)

#     class Meta:
#         model = User
#         # List all of the fields that could possibly be included in a request
#         # or response, including fields specified explicitly above.
#         fields = ['email', 'password', 'token',
#                   'name', 'mobile', 'dob', 'roleid']

#     def create(self, validated_data):
#         log.info("create function has been called of serializer")
#         # Use the `create_user` method we wrote earlier to create a new user.
#         return User.objects.create_user(**validated_data)


# class LoginSerializer(serializers.Serializer):
#     log.info("login serializer")
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(
#         required=True, allow_blank=True, write_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)
#     userstatus = serializers.IntegerField(required=False)

#     def validate(self, data):
#         log.info("login serializer validate function %s", data)
#         email = data['email']
#         password = data.get("password")
#         log.info(email)
#         log.info("password")
#         log.info(password)

#         if email is None:
#             raise serializers.ValidationError(
#                 'An email address is required to log in.'
#             )

#         # Raise an exception if a
#         # password is not provided.
#         if password is None:
#             raise serializers.ValidationError(
#                 'A password is required to log in.'
#             )
#         user = authenticate(email=email, password=password)
#         if user is None:
#             raise serializers.ValidationError(
#                 'A user with this email and password was not found.'
#             )
#         return {
#             'email': user.email,
#             'token': user.token,
#             'userstatus': user.userstatus
#         }


# class UserUpdateSerilalizer(serializers.Serializer):
#     name = serializers.CharField(required=True)
#     mobile = serializers.CharField(required=True)
