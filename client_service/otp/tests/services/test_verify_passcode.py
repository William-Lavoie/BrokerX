from unittest.mock import MagicMock

import pytest
from client.adapters.result import Result
from otp.domain.ports.otp_repository import OTPDTO
from otp.services.verify_passcode import VerifyPassCode

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

    result = use_case.execute(
        "54cc5b84-5720-4c43-af3f-1ef8d13a440c", "test@email.com", "secret"
    )

    assert result.message == "You have entered the correct passcode."
    assert result.code == 200


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

    result = use_case.execute(
        "54cc5b84-5720-4c43-af3f-1ef8d13a440c", "test@email.com", "secret"
    )

    assert (
        result.message
        == "You have made 3 attempts, the passcode has been disabled. You must ask for a new passcode."
    )
    assert result.code == 422


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

    result = use_case.execute(
        "54cc5b84-5720-4c43-af3f-1ef8d13a440c", "test@email.com", "secret"
    )

    assert result.message == "Wrong passcode. Attempts left : 1."
    assert result.code == 422


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

    result = use_case.execute(
        "54cc5b84-5720-4c43-af3f-1ef8d13a440c", "test@email.com", "secret"
    )

    assert result.message == "There was an error, please try again."
    assert result.code == 500


def test_generate_passcode():
    mock_otp_repo = MagicMock()
    mock_client_repo = MagicMock()

    mock_otp_repo.create_passcode.return_value = OTPDTO(
        success=True, code=201, secret="abc1223"
    )

    use_case = VerifyPassCode(
        otp_repository=mock_otp_repo, client_repository=mock_client_repo
    )

    result = use_case.generate_passcode(
        "54cc5b84-5720-4c43-af3f-1ef8d13a440c", "test@email.com"
    )

    assert result.message == "The passcode was sent to your email."
    assert result.code == 201


def test_generate_passcode_failure():
    mock_otp_repo = MagicMock()
    mock_client_repo = MagicMock()

    mock_otp_repo.create_passcode.return_value = OTPDTO(
        success=False, code=500, secret="abc1223"
    )

    use_case = VerifyPassCode(
        otp_repository=mock_otp_repo, client_repository=mock_client_repo
    )

    result = use_case.generate_passcode(
        "54cc5b84-5720-4c43-af3f-1ef8d13a440c", "test@email.com"
    )

    assert result.message == "There was an error, please try again."
    assert result.code == 500
