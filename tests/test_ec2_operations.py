import pytest
from aws_sso_tool.ec2_operations import list_instances, start_instance, stop_instance

def test_list_instances(mocker):
    mock_session = mocker.patch("boto3.Session")
    mock_ec2_client = mock_session.return_value.client.return_value
    mock_ec2_client.describe_instances.return_value = {
        "Reservations": [
            {"Instances": [{"InstanceId": "i-1234567890abcdef0", "State": {"Name": "running"}}]}
        ]
    }
    
    list_instances("test-profile", "us-east-1")
    mock_ec2_client.describe_instances.assert_called_once()

def test_start_instance(mocker):
    mock_session = mocker.patch("boto3.Session")
    mock_ec2_client = mock_session.return_value.client.return_value

    start_instance("test-profile", "i-1234567890abcdef0", "us-east-1")
    mock_ec2_client.start_instances.assert_called_once_with(InstanceIds=["i-1234567890abcdef0"])

def test_stop_instance(mocker):
    mock_session = mocker.patch("boto3.Session")
    mock_ec2_client = mock_session.return_value.client.return_value

    stop_instance("test-profile", "i-1234567890abcdef0", "us-east-1")
    mock_ec2_client.stop_instances.assert_called_once_with(InstanceIds=["i-1234567890abcdef0"])
