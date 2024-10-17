import boto3
from botocore.exceptions import ClientError

def list_buckets(profile, region):
    """ List all S3 buckets in AWS account. """
    session = boto3.Session(profile_name=profile, region_name=region)
    s3_client = session.client('s3')
    buckets = s3_client.list_buckets()
    print("S3 Buckets:")
    for bucket in buckets['Buckets']:
        print(f"  - {bucket['Name']}")

def upload_file(profile, file_path, bucket_name, region, object_name=None):
    """ Upload a file to S3. """
    session = boto3.Session(profile_name=profile, region_name=region)
    s3_client = session.client('s3')
    s3_client.upload_file(file_path, bucket_name, object_name or file_path.split("/")[-1])

def download_file(profile, bucket_name, object_name, file_path, region):
    """ Download a file from S3. """
    session = boto3.Session(profile_name=profile, region_name=region)
    s3_client = session.client('s3')
    s3_client.download_file(bucket_name, object_name, file_path)
