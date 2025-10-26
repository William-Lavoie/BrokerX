from unittest.mock import MagicMock

import pytest
from broker.adapters.result import Result
from broker.domain.ports.otp_repository import OTPDTO
from broker.services.create_account_use_case.verify_passcode import VerifyPassCode

pytestmark = pytest.mark.django_db


def test_execute():
    mock_otp_repo = MagicMock()
    mock_client_repo = MagicMock()

    mock_otp_repo.verify_passcode.return_value = OTPDTO(
        success=True, code=201, secret="abc1223"
    )
    mock_client_repo.update_user_status.return_value = Result(success=True, code=200)

    use_case = VerifyPassCode(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.execute("test@email.com", "secret")

    assert result.success
    assert result.message == "You have entered the correct passcode"


def test_execute_max_attempts():
    mock_otp_repo = MagicMock()
    mock_client_repo = MagicMock()

    mock_otp_repo.verify_passcode.return_value = OTPDTO(
        success=False, code=500, attempts=5
    )
    mock_client_repo.update_user_status.return_value = Result(success=True, code=200)

    use_case = VerifyPassCode(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.execute("test@email.com", "secret")

    assert not result.success
    assert (
        result.message
        == "You have made 3 attempts, the passcode has been disabled. You must ask for a new passcode."
    )


def test_execute_wrong_password():
    mock_otp_repo = MagicMock()
    mock_client_repo = MagicMock()

    mock_otp_repo.verify_passcode.return_value = OTPDTO(
        success=False, code=500, attempts=2
    )
    mock_client_repo.update_user_status.return_value = Result(success=True, code=200)

    use_case = VerifyPassCode(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.execute("test@email.com", "secret")

    assert not result.success
    assert result.message == "Wrong passcode. Attempts left : 1"


def test_execute_user_not_updated():
    mock_otp_repo = MagicMock()
    mock_client_repo = MagicMock()

    mock_otp_repo.verify_passcode.return_value = OTPDTO(
        success=True, code=200, attempts=2
    )
    mock_client_repo.update_user_status.return_value = Result(success=False, code=500)

    use_case = VerifyPassCode(
        client_repository=mock_client_repo, otp_repository=mock_otp_repo
    )

    result = use_case.execute("test@email.com", "secret")

    assert not result.success
    assert result.message == "There was an error, please try again."
