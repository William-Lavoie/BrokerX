import pyotp
import pytest
from client.adapters.django_client_repository import DjangoClientRepository
from client.models import Client
from django.contrib.auth.models import User
from otp.adapters.email_otp_repository import EmailOTPRepository
from otp.models import OTP
from otp.services.verify_passcode import VerifyPassCode

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def setup_function(db):
    user = User.objects.create(
        first_name="John",
        last_name="Smith",
        email="john_smith@example.com",
    )

    Client.objects.create(
        user=user,
        client_id="54cc5b84-5720-4c43-af3f-1ef8d13a440c",
        first_name="John",
        last_name="Smith",
        email="john_smith@example.com",
        address="456 Privett Drive",
        birth_date="1978-01-01",
        phone_number="123-456-7890",
        status="fictional",
    )
    yield


def test_execute():
    OTP.objects.create(
        client_id="54cc5b84-5720-4c43-af3f-1ef8d13a440c",
        secret="JBSWY3DPEHPK3PXP",
        number_attempts=0,
    )

    use_case = VerifyPassCode(EmailOTPRepository(), DjangoClientRepository())

    result = use_case.execute(
        client_id="54cc5b84-5720-4c43-af3f-1ef8d13a440c",
        email="john_smith@example.com",
        passcode=pyotp.TOTP(s="JBSWY3DPEHPK3PXP", interval=600, digits=6).now(),
    )

    assert result.code == 200
    assert result.success
    assert result.message == "You have entered the correct passcode"
