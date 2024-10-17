import os
import logging
import boto3
from botocore.exceptions import ClientError

# נתיב לקובץ שיאחסן את שם הפרופיל שנבחר
DEFAULT_PROFILE_PATH = os.path.expanduser("~/.aws_sso_default_profile")
DEFAULT_REGION_PATH = os.path.expanduser("~/.aws_sso_default_region")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def choose_profile():
    """ Prompt the user to enter their AWS profile name. """
    profile = input("Please enter your AWS profile name: ")
    
    # שמירת הפרופיל שנבחר כ-default
    with open(DEFAULT_PROFILE_PATH, 'w') as f:
        f.write(profile)
    
    return profile

def get_default_profile():
    """ Get default AWS profile from file or prompt the user to enter one. """
    if os.path.exists(DEFAULT_PROFILE_PATH):
        try:
            with open(DEFAULT_PROFILE_PATH, 'r') as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Failed to read default profile from file: {e}")
    
    # אם אין פרופיל מוגדר, נבקש מהמשתמש להזין אחד
    return choose_profile()

def choose_region():
    """ Fetch regions from AWS and prompt the user to choose. """
    ec2 = boto3.client('ec2')
    try:
        response = ec2.describe_regions()
        regions = [region['RegionName'] for region in response['Regions']]
        for i, region in enumerate(regions):
            print(f"{i + 1}. {region}")
        
        while True:
            try:
                choice = int(input("Choose region (number): "))
                if 1 <= choice <= len(regions):
                    selected_region = regions[choice - 1]
                    # שמירה לברירת מחדל בקובץ
                    with open(DEFAULT_REGION_PATH, 'w') as f:
                        f.write(selected_region)
                    return selected_region
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(regions)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    except ClientError as e:
        logger.error(f"Failed to retrieve regions: {e}")
        return None

def get_default_region():
    """ Get default AWS region from file or prompt the user to choose. """
    if os.path.exists(DEFAULT_REGION_PATH):
        try:
            with open(DEFAULT_REGION_PATH, 'r') as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Failed to read default region from file: {e}")
    
    # אם אין קובץ ברירת מחדל או שקראתו נכשלה, נבקש מהמשתמש לבחור ריג'ון
    return choose_region()

