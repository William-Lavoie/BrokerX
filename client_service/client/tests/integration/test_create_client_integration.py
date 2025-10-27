import pytest
from client.adapters.django_client_repository import DjangoClientRepository
from client.models import User
from client.services.create_client import CreateClientUseCase
from otp.adapters.email_otp_repository import EmailOTPRepository

pytestmark = pytest.mark.django_db


def test_execute():
    use_case = CreateClientUseCase(DjangoClientRepository(), EmailOTPRepository())
    result = use_case.execute(
        first_name="John",
        last_name="Smith",
        address="123 Main St",
        birth_date="1990-01-01",
        email="john@example.com",
        phone_number="1234567890",
        password="securepassword",
    )

    assert result.success
    assert result.message == "The user was successfully created"

    user = User.objects.get(email="john@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Smith"
    assert user.email == "john@example.com"
