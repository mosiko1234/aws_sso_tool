import boto3
import logging
from botocore.exceptions import ClientError

# הגדרת מערכת לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_buckets(profile, region):
    """ List all S3 buckets in AWS account. """
    session = boto3.Session(profile_name=profile, region_name=region)
    s3_client = session.client('s3')
    
    try:
        buckets = s3_client.list_buckets()
        logger.info("S3 Buckets:")
        if 'Buckets' in buckets:
            for bucket in buckets['Buckets']:
                logger.info(f"  - {bucket['Name']}")
        else:
            logger.info("No buckets found.")
    except ClientError as e:
        logger.error(f"Failed to list buckets: {e}")

def upload_file(profile, file_path, bucket_name, region, object_name=None):
    """ Upload a file to S3. """
    session = boto3.Session(profile_name=profile, region_name=region)
    s3_client = session.client('s3')
    object_name = object_name or file_path.split("/")[-1]
    
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        logger.info(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except ClientError as e:
        logger.error(f"Failed to upload file {file_path} to {bucket_name}: {e}")
    except FileNotFoundError as e:
        logger.error(f"File {file_path} not found: {e}")
    except Exception as e:
        logger.error(f"An error occurred while uploading file {file_path}: {e}")

def download_file(profile, bucket_name, object_name, file_path, region):
    """ Download a file from S3. """
    session = boto3.Session(profile_name=profile, region_name=region)
    s3_client = session.client('s3')

    try:
        s3_client.download_file(bucket_name, object_name, file_path)
        logger.info(f"File {object_name} downloaded from {bucket_name} to {file_path}")
    except ClientError as e:
        logger.error(f"Failed to download file {object_name} from {bucket_name}: {e}")
    except FileNotFoundError as e:
        logger.error(f"Destination path {file_path} not found: {e}")
    except Exception as e:
        logger.error(f"An error occurred while downloading file {object_name}: {e}")
