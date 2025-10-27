from decimal import Decimal

import pytest
from wallet.adapters.dao.mysql_transaction_dao import MySQLTransactionDAO

pytestmark = pytest.mark.django_db

from wallet.models import Transaction


@pytest.fixture(autouse=True)
def setup_function(db):
    Transaction.objects.create(
        client_id="28877641-1cb6-4d40-971d-e7e9866f9a9f",
        amount=Decimal("10.50"),
        idempotency_key="e4b88817-a42a-4450-87de-fb1f734d57a6",
        message="This is a test",
    )
    yield


def test_write_transaction():
    dao = MySQLTransactionDAO()

    result = dao.write_transaction(
        client_id="28877641-1cb6-4d40-971d-e7e9866f9a9f",
        amount=Decimal("20.99"),
        idempotency_key="43b80e5d-ae6c-4789-a696-2fd81db4296e",
    )

    assert result.success
    assert result.code == 201
    assert result.amount.compare(Decimal("20.99")) == 0
    assert result.status == "P"
    assert not result.message

    saved_transaction = Transaction.objects.filter(
        idempotency_key="43b80e5d-ae6c-4789-a696-2fd81db4296e"
    )

    assert saved_transaction.count() == 1

    saved_transaction = saved_transaction.first()

    assert saved_transaction.amount.compare(Decimal("20.99")) == 0
    assert saved_transaction.status == "P"
    assert (
        str(saved_transaction.idempotency_key) == "43b80e5d-ae6c-4789-a696-2fd81db4296e"
    )


def test_write_transaction_same_uuid():
    dao = MySQLTransactionDAO()

    result = dao.write_transaction(
        client_id="28877641-1cb6-4d40-971d-e7e9866f9a9f",
        amount=Decimal("20.99"),
        idempotency_key="e4b88817-a42a-4450-87de-fb1f734d57a6",
    )

    assert result.success
    assert result.code == 200
    assert result.amount.compare(Decimal("10.50")) == 0
    assert result.status == "P"
    assert result.message == "This is a test"

    saved_transaction = Transaction.objects.filter(
        idempotency_key="e4b88817-a42a-4450-87de-fb1f734d57a6"
    )

    assert saved_transaction.count() == 1


def test_write_transaction_no_user():
    dao = MySQLTransactionDAO()

    result = dao.write_transaction(
        client_id="28877641-1cb6-4d40-971d-e7e9866f9a9f",
        amount=Decimal("20.99"),
        idempotency_key="be3fcd15-9012-4666-8803-fcb2d5686f60",
    )

    assert result.success
    assert result.code == 201
    assert Decimal(result.amount) == Decimal("20.99")


def test_write_transaction_bad_uuid():
    dao = MySQLTransactionDAO()

    result = dao.write_transaction(
        client_id="28877641-1cb6-4d40-971d-e7e9866f9a9f",
        amount=Decimal(20.99),
        idempotency_key="not a uuid",
    )

    assert not result.success
    assert result.code == 400


def test_validate_transaction():
    dao = MySQLTransactionDAO()

    result = dao.validate_transaction("e4b88817-a42a-4450-87de-fb1f734d57a6")

    assert result.success
    assert result.code == 200

    saved_transaction = Transaction.objects.get(
        idempotency_key="e4b88817-a42a-4450-87de-fb1f734d57a6"
    )

    assert saved_transaction.status == "C"


def test_validate_transaction_no_transaction():
    dao = MySQLTransactionDAO()

    result = dao.validate_transaction("5b0d7fcd-f460-413c-bcc6-4d3dcdb29c3c")

    assert not result.success
    assert result.code == 404


def test_validate_transaction_invalid_uuid():
    dao = MySQLTransactionDAO()

    result = dao.validate_transaction("e4efw57a6")

    assert not result.success
    assert result.code == 400


def test_fail_transaction():
    dao = MySQLTransactionDAO()

    result = dao.fail_transaction("e4b88817-a42a-4450-87de-fb1f734d57a6")

    assert result.success
    assert result.code == 200

    saved_transaction = Transaction.objects.get(
        idempotency_key="e4b88817-a42a-4450-87de-fb1f734d57a6"
    )

    assert saved_transaction.status == "F"


def test_fail_transaction_no_transaction():
    dao = MySQLTransactionDAO()

    result = dao.fail_transaction("5b0d7fcd-f460-413c-bcc6-4d3dcdb29c3c")

    assert not result.success
    assert result.code == 404


def test_fail_transaction_invalid_uuid():
    dao = MySQLTransactionDAO()

    result = dao.fail_transaction("e4efw57a6")

    assert not result.success
    assert result.code == 400
