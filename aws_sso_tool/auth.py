import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def configure_sso():
    """ Run AWS SSO configuration command. """
    import subprocess
    subprocess.run(["aws", "configure", "sso"], check=True)

def verify_identity(profile, region):
    """ Verify AWS identity using sts get-caller-identity. """
    session = boto3.Session(profile_name=profile, region_name=region)
    sts_client = session.client('sts')
    try:
        identity = sts_client.get_caller_identity()
        print(f"Successfully connected to AWS as: {identity['Arn']}")
    except (NoCredentialsError, ClientError) as e:
        print(f"Failed to verify identity: {e}")
