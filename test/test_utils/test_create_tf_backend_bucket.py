"""This module contains the test suite for `create_tf_backend_bucket()`."""

import os
from unittest.mock import patch

import botocore
import boto3
from moto import mock_aws
import pytest

from utils.create_tf_backend_bucket import create_tf_backend_bucket


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture
def mock_s3(aws_credentials):
    """Mock s3 client."""
    with mock_aws():
        yield boto3.client("s3", region_name="eu-west-2")


@pytest.mark.describe("create_tf_backend_bucket()")
@pytest.mark.it("should create s3 bucket with name input by user")
@patch("builtins.input", side_effect=["test-tf-backend-bucket"])
def test_creates_bucket(mock_input, mock_s3):
    create_tf_backend_bucket()
    response = mock_s3.list_buckets()
    assert response["Buckets"][0]["Name"] == "test-tf-backend-bucket"
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


@pytest.mark.describe("create_tf_backend_bucket()")
@pytest.mark.it("should raise error if bucket already owned by you")
@patch("builtins.input", side_effect=["test-tf-backend-bucket"])
def test_bucket_already_owned_by_you(mock_input, mock_s3):
    with pytest.raises(mock_s3.exceptions.BucketAlreadyOwnedByYou):
        mock_s3.create_bucket(
            Bucket="test-tf-backend-bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        create_tf_backend_bucket()


@pytest.mark.describe("create_tf_backend_bucket()")
@pytest.mark.it("should raise error if given invalid bucket name")
@patch("builtins.input", side_effect=["ab"])
def test_invalid_bucket_name(mock_input, mock_s3):
    with pytest.raises(mock_s3.exceptions.ClientError):
        create_tf_backend_bucket()


@pytest.mark.describe("create_tf_backend_bucket()")
@pytest.mark.it("should raise error if given invalid characters")
@patch("builtins.input", side_effect=["$$$$"])
def test_invalid_characters(mock_input, mock_s3):
    with pytest.raises(botocore.exceptions.ParamValidationError):
        create_tf_backend_bucket()
