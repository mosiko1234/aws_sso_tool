import os
import subprocess
import click
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import configparser

# הגדרות ברירת מחדל של פרופיל ואזור
DEFAULT_PROFILE_PATH = os.path.expanduser("~/.aws_sso_default_profile")
DEFAULT_REGION_PATH = os.path.expanduser("~/.aws_sso_default_region")

def run_aws_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Error: {result.stderr}")
        return result.stdout
    except Exception as e:
        click.echo(f"Failed to run command: {str(e)}")
        return None

def configure_sso():
    click.echo("Starting AWS SSO configuration...")
    command = ["aws", "configure", "sso"]
    output = run_aws_command(command)
    if output:
        click.echo(output)
    else:
        click.echo("SSO configuration failed.")

def verify_identity(profile, region):
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        sts_client = session.client('sts')
        identity = sts_client.get_caller_identity()
        click.echo(f"Successfully connected to AWS as: {identity['Arn']}")
    except NoCredentialsError:
        click.echo("Error: AWS credentials not found.")
    except ClientError as e:
        click.echo(f"Error in connecting: {e}")

def get_profiles():
    config_path = os.path.expanduser("~/.aws/config")
    config = configparser.ConfigParser()
    config.read(config_path)
    profiles = [section.replace("profile ", "") for section in config.sections() if section.startswith("profile ")]
    return profiles

def get_default_profile():
    if os.path.exists(DEFAULT_PROFILE_PATH):
        with open(DEFAULT_PROFILE_PATH, 'r') as file:
            return file.read().strip()
    return None

def set_default_profile(profile):
    with open(DEFAULT_PROFILE_PATH, 'w') as file:
        file.write(profile)

def get_default_region():
    if os.path.exists(DEFAULT_REGION_PATH):
        with open(DEFAULT_REGION_PATH, 'r') as file:
            return file.read().strip()
    return None

def set_default_region(region):
    with open(DEFAULT_REGION_PATH, 'w') as file:
        file.write(region)

def get_available_regions():
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_regions()
        regions = [region['RegionName'] for region in response['Regions']]
        return regions
    except ClientError as e:
        click.echo(f"Error fetching regions: {e}")
        return ['us-east-1', 'us-west-1', 'eu-west-1', 'ap-southeast-1']

def choose_region():
    regions = get_available_regions()
    if not regions:
        click.echo("Could not retrieve regions from AWS.")
        return None
    
    click.echo("Choose an AWS region:")
    for idx, region in enumerate(regions, 1):
        click.echo(f"{idx}. {region}")

    region_choice = click.prompt("Enter the number of the region", type=int)
    chosen_region = regions[region_choice - 1]

    set_default_region(chosen_region)
    click.echo(f"Region '{chosen_region}' set as default.")
    
    return chosen_region

# S3 operations
def list_s3_buckets(profile, region):
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        s3_client = session.client('s3')
        buckets = s3_client.list_buckets()
        click.echo("S3 Buckets:")
        for bucket in buckets['Buckets']:
            click.echo(f"  - {bucket['Name']}")
    except ClientError as e:
        click.echo(f"Failed to list S3 buckets: {e}")

def upload_file(profile, file_path, bucket_name, region, object_name=None):
    if object_name is None:
        object_name = file_path.split("/")[-1]
    
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        s3_client = session.client('s3')
        s3_client.upload_file(file_path, bucket_name, object_name)
        click.echo(f"File {file_path} uploaded to {bucket_name}/{object_name}.")
    except ClientError as e:
        click.echo(f"Failed to upload file: {e}")

def download_file(profile, bucket_name, object_name, file_path, region):
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        s3_client = session.client('s3')
        s3_client.download_file(bucket_name, object_name, file_path)
        click.echo(f"File {object_name} downloaded to {file_path}.")
    except ClientError as e:
        click.echo(f"Failed to download file: {e}")

# EC2 operations
def list_instances(profile, region):
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        ec2_client = session.client('ec2')
        instances = ec2_client.describe_instances()
        
        click.echo("EC2 Instances:")
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                click.echo(f"  - Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")
    except ClientError as e:
        click.echo(f"Failed to list EC2 instances: {e}")

def start_instance(profile, instance_id, region):
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        ec2_client = session.client('ec2')
        ec2_client.start_instances(InstanceIds=[instance_id])
        click.echo(f"Instance {instance_id} started.")
    except ClientError as e:
        click.echo(f"Failed to start instance: {e}")

def stop_instance(profile, instance_id, region):
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        ec2_client = session.client('ec2')
        ec2_client.stop_instances(InstanceIds=[instance_id])
        click.echo(f"Instance {instance_id} stopped.")
    except ClientError as e:
        click.echo(f"Failed to stop instance: {e}")

# Main function with region prompt and set-region option
@click.command()
@click.option('--set-default', is_flag=True, help='Set a default AWS profile.')
@click.option('--set-region', is_flag=True, help='Set a default AWS region.')
@click.option('--list-buckets', 'list_buckets_option', is_flag=True, help='List S3 buckets.')  # תיקון כאן
@click.option('--upload-file', type=(str, str), help='Upload file to S3 (provide file_path and bucket_name).')
@click.option('--download-file', type=(str, str, str), help='Download file from S3 (provide bucket_name, object_name, file_path).')
@click.option('--list-instances', is_flag=True, help='List EC2 instances.')
@click.option('--start-instance', type=str, help='Start an EC2 instance (provide instance_id).')
@click.option('--stop-instance', type=str, help='Stop an EC2 instance (provide instance_id).')
def main(set_default, set_region, list_buckets_option, upload_file, download_file, list_instances, start_instance, stop_instance):  # תיקון כאן
    profiles = get_profiles()

    if not profiles:
        click.echo("No profiles found. Please run 'aws configure sso' first.")
        configure_sso()
        profiles = get_profiles()  # Reload profiles after configuration

    if set_default:
        click.echo("Choose a profile to set as default:")
        for idx, profile in enumerate(profiles, 1):
            click.echo(f"{idx}. {profile}")
        
        profile_choice = click.prompt("Enter the number of the profile", type=int)
        chosen_profile = profiles[profile_choice - 1]
        set_default_profile(chosen_profile)
        click.echo(f"Profile '{chosen_profile}' set as default.")
        return

    if set_region:
        region = choose_region()
        return

    default_profile = get_default_profile()

    if default_profile:
        profile = default_profile
        click.echo(f"Using default profile: {profile}")
    else:
        click.echo("No default profile found. Choose a profile:")
        for idx, profile in enumerate(profiles, 1):
            click.echo(f"{idx}. {profile}")

        profile_choice = click.prompt("Enter the number of the profile", type=int)
        profile = profiles[profile_choice - 1]

    # Choose the region
    region = get_default_region()
    if not region:
        region = choose_region()

    if list_buckets_option:  # שינוי כאן
        list_s3_buckets(profile, region)
        return
    if upload_file:
        file_path, bucket_name = upload_file
        upload_file(profile, file_path, bucket_name, region)
        return
    if download_file:
        bucket_name, object_name, file_path = download_file
        download_file(profile, bucket_name, object_name, file_path, region)
        return

    if list_instances:
        list_instances(profile, region)
        return
    if start_instance:
        start_instance(profile, start_instance, region)
        return
    if stop_instance:
        stop_instance(profile, stop_instance, region)
        return

    verify_identity(profile, region)

if __name__ == '__main__':
    main()
