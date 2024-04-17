"""This module contains the definition for `create_tf_backend_bucket()`."""

from pprint import pprint

import boto3

def create_tf_backend_bucket():

    bucket_name = input("Please enter name for terraform backend bucket: ")

    s3 = boto3.client("s3", region_name="eu-west-2")
    
    response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})
    
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        print(f"✅ {bucket_name} successfully created.")
