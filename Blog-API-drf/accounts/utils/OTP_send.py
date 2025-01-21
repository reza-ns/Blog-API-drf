# Send OTP code by email or sms and save it in redis.
# Verify given code by compare it with code that saved in redis.
import redis

# r = redis.Redis()

def sms_otp_send(phone_number):
    ...

def sms_otp_verify(phone_number, code):
    ...

def email_otp_send(email):
    ...

def email_otp_verify(email, code):
    ...
