import pyotp
import pytest
from broker.adapters.django_client_repository import DjangoClientRepository
from broker.adapters.email_otp_repository import EmailOTPRepository
from broker.models import Client, ClientOTP
from broker.services.create_account_use_case.verify_passcode import VerifyPassCode
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_execute():
    user = User.objects.create_user(
        first_name="John",
        last_name="Smith",
        email="test@email.com",
        username="john.smith",
        password="123abc",
    )

    Client.objects.create(
        user=user,
        phone_number="123",
        birth_date="2002-01-01",
        address="539 Sherbrooke",
        status="P",
    )

    ClientOTP.objects.create(user=user, secret="JBSWY3DPEHPK3PXP", number_attempts=0)

    use_case = VerifyPassCode(EmailOTPRepository(), DjangoClientRepository())

    result = use_case.execute(
        "test@email.com", pyotp.TOTP(s="JBSWY3DPEHPK3PXP", interval=600, digits=6).now()
    )

    assert result.success
    assert result.message == "You have entered the correct passcode"
