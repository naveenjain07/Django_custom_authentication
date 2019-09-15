import re
import datetime
from django.conf import settings
from django.core.validators import validate_email
log = settings.LOG


def emailValidator(email):
    log.info("email validator")

    if email is None or email == "":
        raise Exception({"error": "email_cannot_blank"})
    if isinstance(email, str) == False:
        raise Exception({"error": "email_string_format"})
    try:
        validate_email(email)
    except:
        raise Exception({"error": "email_pattern_invalid"})

    # if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    #     raise Exception({"error": "email_pattern_invalid"})
        # return False, "email_pattern_invalid"
    return True


def passwordValidator(password):
    log.info("password validator")
    if password == "" or password is None:
        raise Exception({"error": "password_cannot_blank"})
    if isinstance(password, str) == False:
        raise Exception({"error": "password_string_format"})
    if len(password) < 8 or len(password) > 18:
        raise Exception({"error": "password_length_8_to_18"})
    if not re.match(r'^((?!.*[\s])(?=.*[a-z A-Z])(?=.*\d).{8})', password):
        raise Exception({"error": "password_invalid_pattern"})
    return True


def dateValidator(date):
    log.info("date validator")
    if date == "" or date is None:
        raise Exception({"error": "date_cannot_blank"})
    if isinstance(date, str) == False:
        raise Exception({"error": "date_string_format"})
    try:
        log.info(datetime.datetime.strptime(date, '%Y-%m-%d'))
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except:
        raise Exception({"error": "date_pattern_invalid"})


def mobileValidator(mobile):
    log.info("mobile validator")
    if mobile == "" or mobile is None:
        raise Exception({"error": "mobile_cannot_blank"})
    if isinstance(mobile, str) == False:
        raise Exception({"error": "mobile_string_format"})
    if not re.match(r'^\+{0,1}[0-9]{8,16}$', mobile):
        raise Exception({"error": "mobile_invalid_pattern"})
    return True
