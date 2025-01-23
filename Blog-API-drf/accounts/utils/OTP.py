# Send OTP code by email or sms and save it in redis.
# Verify given code by compare it with code that saved in redis.

def sms_otp_send(phone_number):
    """
    Generate and send opt_code by sms
    :param phone_number: user phone number
    :return: generated otp code
    """
    return 12345

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
    return 54321

def email_otp_verify(email, code):
    """
    Compare and verify code saved in redis and user given code
    :param email: user email
    :param code: user given code
    :return: boolean
    """
    ...

def generate_otp_code():
    ...
