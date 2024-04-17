"""This module contains the definition for `create_tf_backend_bucket()`."""

import botocore
import boto3


def create_tf_backend_bucket():
    """A function to create an s3 bucket in AWS to hold terraform backend.
    - User will be prompted to inpute bucket name into console.
    - A bucket will then be created with that name in the configured AWS account.
    - Bucket versioning is then enabled in the created bucket.

    Raises:
        b1: BucketAlreadyOwnedByYou - if a bucket with given name already exists in AWS account.
        b2: BucketAlreadyExists - if a bucket with the given name already exists.
        c: ClientError - if the given bucket name is too long or short.
        p: ParamValidationError - if the given bucket name fails AWS regex check.
    """

    bucket_name = input("Please enter name for terraform backend bucket: ")

    s3 = boto3.client("s3", region_name="eu-west-2")

    try:
        response = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        s3 = boto3.resource("s3")
        versioning = s3.BucketVersioning(bucket_name)
        versioning.enable()

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print(f"✅ {bucket_name} successfully created.")

    except s3.exceptions.BucketAlreadyOwnedByYou as b1:
        print(f"❌ {bucket_name} already owned by you - please try again.")
        raise b1

    except s3.exceptions.BucketAlreadyExists as b2:
        print(f"❌ {bucket_name} already exists - please try again.")
        raise b2

    except botocore.exceptions.ClientError as c:
        if "InvalidBucketName" in str(c):
            print(f"❌ `{bucket_name}` is not a valid bucket name - please try again.")
            print(
                "https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html"
            )
            raise c

    except botocore.exceptions.ParamValidationError as p:
        print(f"❌ `{bucket_name}` contains invalid characters - please try again.")
        print(
            "https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html"
        )
        raise p


if __name__ == "__main__":
    create_tf_backend_bucket()
