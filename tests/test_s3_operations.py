import pytest
from aws_sso_tool.s3_operations import list_buckets, upload_file, download_file

def test_list_buckets(mocker):
    mock_session = mocker.patch("boto3.Session")
    mock_s3_client = mock_session.return_value.client.return_value
    mock_s3_client.list_buckets.return_value = {"Buckets": [{"Name": "bucket1"}, {"Name": "bucket2"}]}
    
    list_buckets("test-profile", "us-east-1")
    mock_s3_client.list_buckets.assert_called_once()

def test_upload_file(mocker):
    mock_session = mocker.patch("boto3.Session")
    mock_s3_client = mock_session.return_value.client.return_value

    upload_file("test-profile", "/path/to/file", "test-bucket", "us-east-1")
    mock_s3_client.upload_file.assert_called_once_with("/path/to/file", "test-bucket", "file")

def test_download_file(mocker):
    mock_session = mocker.patch("boto3.Session")
    mock_s3_client = mock_session.return_value.client.return_value

    download_file("test-profile", "test-bucket", "object", "/path/to/save", "us-east-1")
    mock_s3_client.download_file.assert_called_once_with("test-bucket", "object", "/path/to/save")
