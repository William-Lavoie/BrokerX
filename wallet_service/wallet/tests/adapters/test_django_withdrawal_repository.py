from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from wallet.adapters.django_withdrawal_repository import \
    DjangoWithdrawalRepository
from wallet.domain.ports.withdrawal_repository import WithdrawalDTO

pytestmark = pytest.mark.django_db


def test_write_withdrawal():
    mock_dao = MagicMock()
    mock_dao.write_withdrawal.return_value = WithdrawalDTO(success=True, code=201)

    repo = DjangoWithdrawalRepository(dao=mock_dao)

    withdrawal_dto = repo.write_withdrawal(
        "f551a526-0deb-42d6-98b9-06f3fcc8cdb5",
        Decimal("10.99"),
        "abcdefghijklmnopqrstuvwxyz",
    )

    assert withdrawal_dto.success
    assert withdrawal_dto.code == 201

    mock_dao.write_withdrawal.assert_called_once_with(
        client_id="f551a526-0deb-42d6-98b9-06f3fcc8cdb5",
        amount=Decimal("10.99"),
        idempotency_key="abcdefghijklmnopqrstuvwxyz",
    )


def test_update_status():
    mock_dao = MagicMock()
    mock_dao.update_status.return_value = WithdrawalDTO(success=True, code=200)

    repo = DjangoWithdrawalRepository(dao=mock_dao)

    withdrawal_dto = repo.update_status("abcdefghijklmnopqrstuvwxyz", "COMPLETED")

    assert withdrawal_dto.success
    assert withdrawal_dto.code == 200

    mock_dao.update_status.assert_called_once_with(
        "abcdefghijklmnopqrstuvwxyz", "COMPLETED"
    )
