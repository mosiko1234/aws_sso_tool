import subprocess
import os
import json
import time
import click
from pathlib import Path

# הסף שבו נחדש את ה-token (10 דקות לפני שפג תוקף)
TOKEN_EXPIRATION_THRESHOLD = 60 * 10  # 10 דקות (בשניות)

def get_sso_token_expiration(profile):
    """
    מחפש את קובץ ה-SSO cache כדי לבדוק את תוקף ה-token עבור פרופיל מסוים.
    """
    # מסלול תיקיית cache של SSO (תלוי במערכת ההפעלה)
    sso_cache_dir = Path.home() / ".aws" / "sso" / "cache"
    
    # אם התיקיה לא קיימת, נצטרך להתחבר מחדש
    if not sso_cache_dir.exists():
        return None

    # חיפוש קבצי cache לפי פרופיל
    for cache_file in sso_cache_dir.glob("*.json"):
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
            if cache_data.get("startUrl") and profile in cache_data.get("startUrl"):
                # מחזיר את זמן התוקף של ה-token
                return cache_data.get("expiresAt")
    
    return None

def is_sso_token_valid(profile):
    """
    בודק אם ה-Token של AWS SSO בתוקף עבור פרופיל מסוים על סמך זמן התוקף.
    """
    expiration_time_str = get_sso_token_expiration(profile)

    if expiration_time_str is None:
        return False  # אין token, חייבים להתחבר מחדש

    # המרת זמן התוקף למבנה timestamp
    expiration_time = time.mktime(time.strptime(expiration_time_str, "%Y-%m-%dT%H:%M:%SZ"))
    current_time = time.time()

    # בדיקה אם התוקף עומד לפוג
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
