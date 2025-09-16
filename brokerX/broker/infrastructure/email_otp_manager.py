from django.core.mail import send_mail

def send_email_passcode(email: str):
    send_mail(
    "Subject here",
    "Here is the message.",
    "from@example.com",
    [email],
    fail_silently=False,
)