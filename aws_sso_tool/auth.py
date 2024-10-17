import subprocess
import time
import boto3
import click  
from botocore.exceptions import ClientError, NoCredentialsError

TOKEN_EXPIRATION_THRESHOLD = 60 * 10

def is_sso_token_valid(profile):
    """
    בודק אם ה-Token של AWS SSO עדיין בתוקף עבור פרופיל מסוים.
    מחזיר True אם ה-Token תקף, False אם יש לחדש אותו.
    """
    try:
        # יוצרים session עם הפרופיל המוגדר
        session = boto3.Session(profile_name=profile)
        credentials = session.get_credentials()

        # בודקים אם קיימת תוקף של ה-token
        expiration_time = credentials._expiry_time.timestamp()  # תוקף ה-token
        current_time = time.time()  # הזמן הנוכחי

        # אם התוקף קרוב לפוג לפי הסף שהגדרנו, נחזיר False
        return (expiration_time - current_time) > TOKEN_EXPIRATION_THRESHOLD
    except AttributeError:
        return False  # אם אין token זמין, חובה להתחבר מחדש
    except (ClientError, NoCredentialsError) as e:
        print(f"Error checking token validity: {e}")
        return False

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
    פונקציה לבדיקת תוקף ה-token ולחידוש במידת הצורך לפני הפעלת כל פקודה.
    """
    if not is_sso_token_valid(profile):
        renew_sso_token(profile)
    else:
        print("SSO token is still valid.")

def configure_sso():
    """
    Initial configuration for AWS SSO.
    """
    click.echo("Starting AWS SSO configuration...")
    command = ["aws", "configure", "sso"]
    subprocess.run(command, check=True)

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
