from django.conf import settings
from .customValidations import *
from authentication.models import User
import json
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated
log = settings.LOG
STATUS = settings.STATUS


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        roleid = None
        data = request.data
        log.info("signup request data %s", data)

        try:
            # VALIDATION OF DATA FOR USER MODEL
            if 'name' not in data:
                log.info("name required")
                return Response({"error": "name_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                if data['name'] is None or data['name'] == "":
                    log.info("name_cannot_blank")
                    return Response({"error": "name_cannot_blank"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                elif isinstance(data['name'], str) == False:
                    log.info("name_string_format_required")
                    return Response({"error": "name_string_format_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if 'email' not in data:
                log.info("email_required")
                return Response({"error": "email_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                emailValidator(data['email'])
            if 'password' not in data:
                log.info("password_required")
                return Response({"error": "password_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                passwordValidator(data['password'])
            if 'mobile' not in data:
                log.info("mobile_required")
                return Response({"error": "mobile_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                mobileValidator(data['mobile'])
            if 'dob' not in data:
                log.info("dob_required")
                return Response({"error": "dob_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                dateValidator(data['dob'])
            if 'roleid' in data:
                if isinstance(data['roleid'], int) == False:
                    log.info("roleid_should_int_format")
                    return Response({"error": "roleid__int_format_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                else:
                    roleid = data['roleid']
        except Exception as e:
            log.info("__field validation exception__")
            log.info(e.args[0])
            return Response(e.args[0], status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            User.objects.get(email=data['email'])
            log.info("user_already_exist")
            return Response({"error": "user_already_exist"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            pass
        if roleid:
            log.info("creating user with given roleid")
            user = User.objects.create_user(
                name=data['name'], email=data['email'], password=data['password'], dob=data['dob'], mobile=data['mobile'], roleid=data['roleid'], token_type=STATUS.ACCESS_TOKEN_CONFIRMATION)
        else:
            log.info("creating user with default roleid")
            user = User.objects.create_user(
                name=data['name'], email=data['email'], password=data['password'], dob=data['dob'], mobile=data['mobile'], token_type=STATUS.ACCESS_TOKEN_CONFIRMATION)
        log.info("user token %s", user.token)
        try:
            email_body = "body"
            log.info("sending email")
            email_html_msg = render_to_string('email.html')
            email = EmailMultiAlternatives("subject", user.token, 'njain3151@gmail.com',
                                           [user.email])
            email.attach_alternative(email_html_msg, "text/html")
            log.info("sending email to new user")
            email.send()
        except Exception as e:
            log.info("_____error in sending email check mail logs______")
            log.info(e)

        log.info('user added in system with userid %d', user.userid)
        return Response({"message": "sign up successfull & confirmation mail has been sent"}, status=status.HTTP_201_CREATED)
    else:
        log.info("method"+request.method+"not allowed")
        return Response('request method is not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def login(request):
    if request.method == "POST":
        data = request.data
        log.info("login request data %s", data)
        try:
            if 'email' not in data:
                log.info("email_required")
                return Response({"error": "email_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                emailValidator(data['email'])
            if 'password' not in data:
                log.info("password_required")
                return Response({"error": "password_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                passwordValidator(data['password'])
            log.info("authentication checking with email and password")
            user = authenticate(email=data['email'], password=data['password'])

        except Exception as e:
            log.info("field validation exception")
            log.info(e.args[0])
            return Response(e.args[0], status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if user is None:
            log.info("user_not_found_with_credentials")
            return Response({"error": "user_not_found_with_credentials"}, status=status.HTTP_404_NOT_FOUND)
        else:
            user.token_type = STATUS.ACCESS_TOKEN_LOGIN
            user.save()
        if user.userstatus == 2:
            log.info("login_success")
            return_obj = {'message': 'login_success',
                          'user': {
                              'email': user.email,
                              'token': user.token,
                              'userid': user.userid
                          }}
            return Response(return_obj, status=status.HTTP_200_OK)
        else:
            log.info("user_not_active")
            return Response('user_not_active', status=status.HTTP_403_FORBIDDEN)
    else:
        log.info("method "+request.method+"not allowed")
        return Response('method is not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PUT'])
# @login_required()
def updateUserDetails(request, userId):

    if request.method == "PUT":
        if request.auth is None:
            log.info('user is not  authenticated')
            return Response({"error": "user is not  authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.auth[0] != STATUS.ACCESS_TOKEN_LOGIN:
            return Response({"error": "user is unauthorized to access this api"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.userid == userId and request.user.userstatus == 2:
            log.info('user is allowed to use this api with userid %s',
                     str(request.user.userid))
        else:
            log.info('user_details_mismatch_userid_or_user_is_inactive')
            return Response({"error": 'user_details_mismatch_userid_or_user_is_inactive'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        log.info("requested data for update user info %s", data)
        try:

            if "name" in data:
                if data['name'] is None or data['name'] == "":
                    log.info("name_cannot_blank")
                    return Response({"error": "name_cannot_blank"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                elif isinstance(data['name'], str) == False:
                    log.info("name_string_format_required")
                    return Response({"error": "name_string_format_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                request.user.name = data['name']
            if 'mobile' in data:
                mobileValidator(data['mobile'])
                request.user.mobile = data['mobile']
        except Exception as e:
            log.info("field validation exception")
            log.info(e.args[0])
            return Response(e.args[0], status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        log.info("updating the user")
        request.user.save()
        log.info("successful_updated")
        return Response({"message": "successful_updated"}, status=status.HTTP_200_OK)
    else:
        log.info("method"+request.method+"not allowed")
        return Response('method is not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def confirmUser(request):
    if request.method == "POST":
        log.info(request.auth)
        if request.auth is None:
            log.info('user is not  authenticated with confirmation link')
            return Response({"error": "user is not  authenticated with confirmation link"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.auth[0] != STATUS.ACCESS_TOKEN_CONFIRMATION:
            return Response({"error": "user is unauthorized to access this api"}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        log.info("++++++++++++++++++++++++++user_token_type:" + str(request.auth))
        log.info("user status %d of user with user id %d before confirmation",
                 user.userstatus, user.userid)
        if user.userstatus == 1:
            user.userstatus = 2
        else:
            log.info("user is already in active state")
            return Response('user is already in active state', status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        log.info("updating the user status")
        user.save()
        log.info("user_activated")
        return Response('user confirmed and active', status=status.HTTP_202_ACCEPTED)
    else:
        log.info("method"+request.method+"not allowed")

        return Response('method is not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
# forgot and confirmation link
def generateLink(request):
    log.info("forget password request data %s", request.data)
    # token_type = STATUS.ACCESS_TOKEN_FORGOT_PASSWORD
    try:
        if 'email' not in request.data:
            log.info("email_required")
            return Response({"error": "email_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:

            emailValidator(request.data['email'])
        if 'request_type' not in request.data:
            raise Exception({"error": "request_type_required"})
        elif request.data['request_type'] == 1:
            log.info("confirmation link resend requested")
            token_type = STATUS.ACCESS_TOKEN_CONFIRMATION
        elif request.data['request_type'] == 3:
            log.info("confirmation link resend requested")
            token_type = STATUS.ACCESS_TOKEN_FORGOT_PASSWORD
        else:
            raise Exception({"error": "request type is not valid"})
    except Exception as e:
        log.info("field validation exception")
        log.info(e.args[0])
        return Response(e.args[0], status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:
        user = User.objects.get(email=request.data['email'])
        log.info("user_exist")
        if token_type == STATUS.ACCESS_TOKEN_CONFIRMATION and user.userstatus == STATUS.USER_ACTIVE:
            return Response({"error": "user_already_active"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif token_type == STATUS.ACCESS_TOKEN_FORGOT_PASSWORD and user.userstatus == STATUS.USER_INACTIVE:
            return Response({"error": "user_inactive"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        user.token_type = token_type
        user.save()
    except Exception as e:
        log.info("user not found - %s", e)
        return Response({"error": "user_not_found"}, status=status.HTTP_404_NOT_FOUND)

    if token_type == STATUS.ACCESS_TOKEN_CONFIRMATION:
        log_message = 'sending email confirm link'
        subject = "confirm email here"
        email_template = 'email.html'
    elif token_type == STATUS.ACCESS_TOKEN_FORGOT_PASSWORD:
        log_message = 'sending forgot password email link'
        subject = "forgot password"
        email_template = 'email.html'
    try:
        log.info(log_message)
        email_html_msg = render_to_string(email_template)
        email = EmailMultiAlternatives(subject, user.token, 'njain3151@gmail.com',
                                       [user.email])
        email.attach_alternative(email_html_msg, "text/html")
        email.send()
        log.info(" email sent to user")
    except Exception as e:
        log.info("_____error in sending email check mail logs______")
        log.info(e)
        return Response({"error": "error_sending_email"}, status=status.HTTP_417_EXPECTATION_FAILED)

    return Response({"message": "email_sent_successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def resetPassword(request):
    if request.auth is None:
        log.info('user is not  authenticated with reset password token')
        return Response({"error": "user is not  authenticated with reset password token"}, status=status.HTTP_401_UNAUTHORIZED)
    if request.auth[0] != STATUS.ACCESS_TOKEN_FORGOT_PASSWORD:
        return Response({"error": "user is unauthorized to access this api"}, status=status.HTTP_401_UNAUTHORIZED)
    log.info("reset password request data %s", request.data)
    if 'password' not in request.data:
        log.info("password_required")
        return Response({"error": "password_required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    else:
        try:

            passwordValidator(request.data['password'])
        except Exception as e:
            log.info("field validation exception")
            log.info(e.args[0])
            return Response(e.args[0], status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:
        user = User.objects.get(userid=request.user.userid)
        log.info("user_exist")
        user.set_password(request.data['password'])
        user.save()
    except Exception as e:
        log.info("user not found - %s", e)
        return Response({"error": "user_not_found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        log.info("sending email password has been reset")
        email_html_msg = render_to_string('email.html')
        email = EmailMultiAlternatives("subject", None, 'njain3151@gmail.com',
                                       [user.email])
        email.attach_alternative(email_html_msg, "text/html")
        email.send()
        log.info(" email sent to user")
    except Exception as e:
        log.info("_____error in sending email check mail logs______")
        log.info(e)
        return Response({"error": "error_sending_email"}, status=status.HTTP_417_EXPECTATION_FAILED)
    return Response({"message": "reset_password_successfully"}, status=status.HTTP_200_OK)
