import random


def sms_otp_send(phone_number):
    """
    Generate and send opt_code by sms
    :param phone_number: user phone number
    :return: generated otp code
    """
    code = random.randint(1000, 9998)
    return str(code)

def sms_otp_verify(phone_number, code):
    """
    Compare and verify code saved in redis and user given code
    :param phone_number: user phone number
    :param code: user given code
    :return: boolean
    """
    ...

def email_otp_send(email):
    """
    Generate and send opt_code by email
    :param email: user email
    :return: generated otp code
    """
    code = random.randint(1000, 9998)
    return str(code)

def email_otp_verify(email, code):
    """
    Compare and verify code saved in redis and user given code
    :param email: user email
    :param code: user given code
    :return: boolean
    """
    ...

