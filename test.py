import pytest
import mock
from aws import * 
from grfd import * 
from util import * 

def test_get_aws_credentials():
    with mock.patch('yourmodule.aws.get_aws_credentials') as mock_get_aws_credentials:
        mock_get_aws_credentials.return_value = ("mock_s3client", "mock_s3resource")
        result = get_aws_credentials()
        assert result == ("mock_s3client", "mock_s3resource")

def test_check_grfd_credential():
    with mock.patch('yourmodule.grfd.check_grfd_credential') as mock_check_grfd_credential:
        mock_check_grfd_credential.return_value = True
        assert check_grfd_credential() == True

def test_list_buckets():
    with mock.patch('yourmodule.aws.list_buckets') as mock_list_buckets:
        mock_list_buckets.return_value = ["bucket1", "bucket2", "bucket3"]
        assert list_buckets("mock_s3resource") == ["bucket1", "bucket2", "bucket3"]
