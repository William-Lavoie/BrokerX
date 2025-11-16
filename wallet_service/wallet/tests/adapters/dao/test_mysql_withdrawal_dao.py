from decimal import Decimal

import pytest
from wallet.adapters.dao.mysql_withdrawal_dao import MySQLWithdrawalDAO

pytestmark = pytest.mark.django_db

from wallet.models import Withdrawal


@pytest.fixture(autouse=True)
def setup_function(db):
    Withdrawal.objects.create(
        client_id="28877641-1cb6-4d40-971d-e7e9866f9a9f",
        amount=Decimal("10.50"),
        idempotency_key="e4b88817-a42a-4450-87de-fb1f734d57a6",
        message="This is a test",
    )
    yield


def test_write_withdrawal():
    dao = MySQLWithdrawalDAO()

    result = dao.write_withdrawal(
        client_id="28877641-1cb6-4d40-971d-e7e9866f9a9f",
        amount=Decimal("20.99"),
        idempotency_key="43b80e5d-ae6c-4789-a696-2fd81db4296e",
    )

    assert result.success
    assert result.code == 201
    assert result.amount.compare(Decimal("20.99")) == 0
    assert result.status == "PENDING"
    assert not result.message

    saved_withdrawal = Withdrawal.objects.filter(
        idempotency_key="43b80e5d-ae6c-4789-a696-2fd81db4296e"
    )

    assert saved_withdrawal.count() == 1

    saved_withdrawal = saved_withdrawal.first()

    assert saved_withdrawal.amount.compare(Decimal("20.99")) == 0
    assert saved_withdrawal.status == "PENDING"
    assert (
        str(saved_withdrawal.idempotency_key) == "43b80e5d-ae6c-4789-a696-2fd81db4296e"
    )


def test_write_withdrawal_same_uuid():
    dao = MySQLWithdrawalDAO()

    result = dao.write_withdrawal(
        client_id="28877641-1cb6-4d40-971d-e7e9866f9a9f",
        amount=Decimal("20.99"),
        idempotency_key="e4b88817-a42a-4450-87de-fb1f734d57a6",
    )

    assert result.success
    assert result.code == 200
    assert result.amount.compare(Decimal("10.50")) == 0
    assert result.status == "PENDING"
    assert result.message == "This is a test"

    saved_withdrawal = Withdrawal.objects.filter(
        idempotency_key="e4b88817-a42a-4450-87de-fb1f734d57a6"
    )

    assert saved_withdrawal.count() == 1


def test_write_withdrawal_no_user():
    dao = MySQLWithdrawalDAO()

    result = dao.write_withdrawal(
        client_id="28877641-1cb6-4d40-971d-e7e9866f9a9f",
        amount=Decimal("20.99"),
        idempotency_key="be3fcd15-9012-4666-8803-fcb2d5686f60",
    )

    assert result.success
    assert result.code == 201
    assert Decimal(result.amount) == Decimal("20.99")


def test_write_withdrawal_bad_uuid():
    dao = MySQLWithdrawalDAO()

    result = dao.write_withdrawal(
        client_id="28877641-1cb6-4d40-971d-e7e9866f9a9f",
        amount=Decimal(20.99),
        idempotency_key="not a uuid",
    )

    assert not result.success
    assert result.code == 400


def test_update_status():
    dao = MySQLWithdrawalDAO()

    result = dao.update_status("e4b88817-a42a-4450-87de-fb1f734d57a6", "COMPLETED")

    assert result.success
    assert result.code == 200

    saved_withdrawal = Withdrawal.objects.get(
        idempotency_key="e4b88817-a42a-4450-87de-fb1f734d57a6"
    )

    assert saved_withdrawal.status == "COMPLETED"


def test_update_status_no_withdrawal():
    dao = MySQLWithdrawalDAO()

    result = dao.update_status("5b0d7fcd-f460-413c-bcc6-4d3dcdb29c3c", "COMPLETED")

    assert not result.success
    assert result.code == 404


def test_update_status_invalid_uuid():
    dao = MySQLWithdrawalDAO()

    result = dao.update_status("e4efw57a6", "COMPLETED")

    assert not result.success
    assert result.code == 400
