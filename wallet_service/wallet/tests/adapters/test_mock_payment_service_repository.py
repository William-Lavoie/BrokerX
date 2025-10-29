from decimal import Decimal

import pytest
from wallet.adapters.mock_payment_service_repository import MockPaymentServiceRepository
from wallet.external_source.mock_payment_service import MockPaymentService

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "amount,expected",
    [
        ("10.00", "Request timed out while withdrawing funds."),
        ("20.00", "Network connection error occurred."),
        ("30.00", "Unauthorized access."),
        ("40.00", "Rate limit exceeded."),
        ("50.00", "Internal server error."),
        ("60.00", "Invalid withdrawal amount."),
        ("70.00", "Account is locked."),
        ("0.00", "Cannot withdraw zero amount."),
        ("-1.00", "The amount to withdraw must be positive."),
        ("1000.01", "Insufficient funds."),
        ("100.00", "Withdrawal of 100.00 successful."),
    ],
)
def test_various_withdrawal_scenarios(amount, expected):
    repo = MockPaymentServiceRepository(payment_service=MockPaymentService())
    response = repo.withdraw_funds("john_smith@example.com", Decimal(amount))
    assert response.message == expected
