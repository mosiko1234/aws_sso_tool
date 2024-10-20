import subprocess
import time
import boto3
import click
from pathlib import Path
import json
import logging
from botocore.exceptions import NoCredentialsError, ClientError

# הסף שבו נחדש את ה-token (10 דקות לפני שפג תוקף)
TOKEN_EXPIRATION_THRESHOLD = 60 * 10  # 10 דקות (בשניות)

# הגדרת logging במקום שימוש ב-print
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_sso_token_expiration(profile):
    """
    מחפש את קובץ ה-SSO cache כדי לבדוק את תוקף ה-token עבור פרופיל מסוים.
    """
    sso_cache_dir = Path.home() / ".aws" / "sso" / "cache"

    if not sso_cache_dir.exists():
        logger.error(f"SSO cache directory {sso_cache_dir} does not exist.")
        return None

    # חיפוש קובצי cache עבור SSO, בדיקה אם יש token שתואם לפרופיל
    for cache_file in sso_cache_dir.glob("*.json"):
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
                # חיפוש התאמה לפי פרופיל (startUrl)
                if cache_data.get("startUrl") and profile in cache_data.get("startUrl"):
                    return cache_data.get("expiresAt")  # מחזירים את זמן תפוגת ה-token
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON file {cache_file}: {e}")
    
    return None

def is_sso_token_valid(profile):
    """
    בודק אם ה-Token של AWS SSO בתוקף עבור פרופיל מסוים על סמך זמן התוקף.
    """
    expiration_time_str = get_sso_token_expiration(profile)

    if expiration_time_str is None:
        logger.info("No valid SSO token found, renewal needed.")
        return False  # אין token, חייבים להתחבר מחדש

    # המרת זמן התוקף למבנה timestamp
    expiration_time = time.mktime(time.strptime(expiration_time_str, "%Y-%m-%dT%H:%M:%SZ"))
    current_time = time.time()

    # אם התוקף עומד לפוג (קרוב לתאריך התפוגה), נבצע חידוש
    time_left = expiration_time - current_time
    if time_left > TOKEN_EXPIRATION_THRESHOLD:
        logger.info(f"SSO token is still valid, expires in {int(time_left / 60)} minutes.")
        return True
    else:
        logger.info(f"SSO token is about to expire in {int(time_left / 60)} minutes.")
        return False

def renew_sso_token(profile):
    """
    מחדשת את ה-SSO Token על ידי הפעלת הפקודה `aws sso login`.
    """
    try:
        logger.info(f"SSO token expired or invalid. Renewing token for profile: {profile}...")
        # הפעלה של aws sso login כדי לחדש את החיבור
        subprocess.run(["aws", "sso", "login", "--profile", profile], check=True)
        logger.info("SSO token renewed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to renew SSO token: {e}")
        raise

def ensure_sso_token(profile):
    """
    בודקת אם ה-token בתוקף ומחדשת אותו במידת הצורך.
    """
    if not is_sso_token_valid(profile):
        renew_sso_token(profile)
    else:
        logger.info("SSO token is valid, no renewal needed.")

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
