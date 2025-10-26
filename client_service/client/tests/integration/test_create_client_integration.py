import pytest
from client.adapters.django_client_repository import DjangoClientRepository
from broker.adapters.email_otp_repository import EmailOTPRepository
from broker.services.commands.create_client_command import CreateClientCommand
from broker.services.create_account_use_case.create_client import CreateClientUseCase
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_execute():
    use_case = CreateClientUseCase(DjangoClientRepository(), EmailOTPRepository())
    result = use_case.execute(make_command())

    assert result.success
    assert result.message == "The user was successfully created"

    user = User.objects.get(email="john@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Smith"
    assert user.email == "john@example.com"


def make_command():
    return CreateClientCommand(
        first_name="John",
        last_name="Smith",
        address="123 Main St",
        birth_date="1990-01-01",
        email="john@example.com",
        phone_number="1234567890",
        password="securepassword",
    )
