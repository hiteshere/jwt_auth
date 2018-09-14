from datetime import datetime
from jwt_auth import settings
from twilio.rest import Client
from celery import shared_task


def write_log(instance, action):
    f = open("user_log.txt", "a")
    email = instance.email if action == "User created" else instance.user.email
    f.write(action + " with id " + str(instance.id) + " and email " + email + " at " + str(datetime.now()) + "\n")


@shared_task
def otp_check(otp):
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = settings.TWILO_SECRET_SID[0]
    auth_token = settings.TWILO_SECRET_TOKEN[0]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=settings.TWILO_MOBILE_NUMBER[0],
        body="User verification code is {}".format(str(otp)),
        to='+918076786402'
    )
    return "OTP send for "