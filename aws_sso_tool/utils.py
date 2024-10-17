import boto3
from botocore.exceptions import ClientError

DEFAULT_REGION_PATH = "~/.aws_sso_default_region"

def choose_region():
    """ Fetch regions from AWS and prompt the user to choose. """
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_regions()
        regions = [region['RegionName'] for region in response['Regions']]
        for i, region in enumerate(regions):
            print(f"{i + 1}. {region}")
        choice = int(input("Choose region: "))
        return regions[choice - 1]
    except ClientError as e:
        print(f"Failed to retrieve regions: {e}")
        return None

def get_default_profile():
    """ Get default AWS profile from file. """
    return "AdministratorAccess-316512528621"

def get_default_region():
    """ Get default AWS region from file or prompt. """
    return "us-east-1"
