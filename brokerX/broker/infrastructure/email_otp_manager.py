from django.core.mail import send_mail
import pyotp

def send_email_passcode(email: str):
    passcode = generate_passcode()
    send_mail(
    "Subject here",
    passcode.now(),
    "from@example.com",
    [email],
    fail_silently=False,
)

def generate_passcode() -> pyotp.TOTP:
    user_secret = pyotp.random_base32()
    return pyotp.TOTP(s=user_secret,
                          interval=600,
                          digits=6)
