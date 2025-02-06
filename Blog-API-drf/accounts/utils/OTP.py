import random


def sms_otp_send(phone_number):
    """
    Generate and send opt_code by sms
    :param phone_number: user phone number
    :return: generated otp code
    """
    code = random.randint(1000, 9998)
    print(code)
    return str(code)

def email_otp_send(email):
    """
    Generate and send opt_code by email
    :param email: user email
    :return: generated otp code
    """
    code = random.randint(1000, 9998)
    print(code)
    return str(code)

