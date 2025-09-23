import json
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from broker.adapters.mock_payment_service_repository import MockPaymentServiceRepository

pytestmark = pytest.mark.django_db


def test_withdraw_funds():
    mock_service = MagicMock()
    mock_service.withdraw_funds.return_value = json.dumps(
        {"success": True, "message": "This is not a drill"}
    )

    repo = MockPaymentServiceRepository(payment_service=mock_service)

    response = repo.withdraw_funds("john_smith@example.com", Decimal("10.00"))

    assert response.success
    assert response.message == "This is not a drill"
    mock_service.withdraw_funds.assert_called_once_with(
        "john_smith@example.com", Decimal("10.00")
    )
