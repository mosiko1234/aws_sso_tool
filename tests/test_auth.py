import pytest
from aws_sso_tool.auth import verify_identity  # הסרנו את הייבוא של configure_sso

def test_verify_identity(mocker):
    mock_session = mocker.patch("boto3.Session")
    mock_sts_client = mock_session.return_value.client.return_value
    mock_sts_client.get_caller_identity.return_value = {"Arn": "test-arn"}
    
    verify_identity("test-profile", "us-east-1")
    mock_sts_client.get_caller_identity.assert_called_once()
