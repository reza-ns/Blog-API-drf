from django.conf import settings
from zeep import Client



def zpal_payment_request(merchant_id, amount, description, user_email, user_phone, callback_url):
    client = Client(settings.ZARINPAL.get('request_url'))
    result = client.service.PaymentRequest(
        merchant_id, amount, description, user_email, user_phone, callback_url
    )
    if result.Status == 100:
        return 'https://www.zarinpal.com/pg/StartPay/' + result.Authority, result.Authority
    else:
        return None, None

def zpal_payment_verify(merchant_id, authority, amount):
    client = Client(settings.ZARINPAL.get('request_url'))
    result = client.service.Paymentverification(merchant_id, authority, amount)
    is_paid = True if result.Status in (100, 101) else False
    return is_paid, result.RefID
