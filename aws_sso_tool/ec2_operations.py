import boto3
from botocore.exceptions import ClientError

def list_instances(profile, region):
    """ List EC2 instances. """
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2_client = session.client('ec2')
    instances = ec2_client.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")

def start_instance(profile, instance_id, region):
    """ Start an EC2 instance. """
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2_client = session.client('ec2')
    ec2_client.start_instances(InstanceIds=[instance_id])

def stop_instance(profile, instance_id, region):
    """ Stop an EC2 instance. """
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2_client = session.client('ec2')
    ec2_client.stop_instances(InstanceIds=[instance_id])
