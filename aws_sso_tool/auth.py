import subprocess
import time
import boto3  # הוספת ייבוא של boto3
import click
from botocore.exceptions import NoCredentialsError, ClientError

# הסף שבו נחדש את ה-token (10 דקות לפני שפג תוקף)
TOKEN_EXPIRATION_THRESHOLD = 60 * 10  # 10 דקות (בשניות)

def get_sso_token_expiration(profile):
    """
    מחפש את קובץ ה-SSO cache כדי לבדוק את תוקף ה-token עבור פרופיל מסוים.
    """
    sso_cache_dir = Path.home() / ".aws" / "sso" / "cache"
    
    if not sso_cache_dir.exists():
        return None

    for cache_file in sso_cache_dir.glob("*.json"):
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
            if cache_data.get("startUrl") and profile in cache_data.get("startUrl"):
                return cache_data.get("expiresAt")
    
    return None

def is_sso_token_valid(profile):
    """
    בודק אם ה-Token של AWS SSO בתוקף עבור פרופיל מסוים על סמך זמן התוקף.
    """
    expiration_time_str = get_sso_token_expiration(profile)

    if expiration_time_str is None:
        return False  # אין token, חייבים להתחבר מחדש

    expiration_time = time.mktime(time.strptime(expiration_time_str, "%Y-%m-%dT%H:%M:%SZ"))
    current_time = time.time()

    return (expiration_time - current_time) > TOKEN_EXPIRATION_THRESHOLD

def renew_sso_token(profile):
    """
    מחדשת את ה-SSO Token על ידי הפעלת הפקודה `aws sso login`.
    """
    try:
        print(f"SSO token expired or invalid. Renewing token for profile: {profile}...")
        subprocess.run(["aws", "sso", "login", "--profile", profile], check=True)
        print("SSO token renewed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to renew SSO token: {e}")
        raise

def ensure_sso_token(profile):
    """
    בודקת אם ה-token בתוקף ומחדשת אותו במידת הצורך.
    """
    if not is_sso_token_valid(profile):
        renew_sso_token(profile)
    else:
        print("SSO token is still valid.")

def verify_identity(profile, region):
    """
    Verify AWS identity using sts get-caller-identity.
    """
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        sts_client = session.client('sts')
        identity = sts_client.get_caller_identity()
        click.echo(f"Successfully connected to AWS as: {identity['Arn']}")
    except NoCredentialsError:
        click.echo("Error: AWS credentials not found.")
    except ClientError as e:
        click.echo(f"Error in connecting: {e}")
