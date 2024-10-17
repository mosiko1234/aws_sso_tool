import click
from .auth import verify_identity, ensure_sso_token
from .s3_operations import list_buckets as list_s3_buckets, upload_file, download_file
from .ec2_operations import list_instances, start_instance, stop_instance
from .utils import choose_region, get_default_profile, get_default_region

@click.command()  # יש לוודא שיש דקורטור שמגדיר את הפקודה הראשית של CLI
@click.option('--set-default', is_flag=True, help='Set a default AWS profile.')
@click.option('--set-region', is_flag=True, help='Set a default AWS region.')
@click.option('--list-buckets', 'list_buckets_option', is_flag=True, help='List S3 buckets.')
@click.option('--upload-file', type=(str, str), help='Upload file to S3 (provide file_path and bucket_name).')
@click.option('--download-file', type=(str, str, str), help='Download file from S3 (provide bucket_name, object_name, file_path).')
@click.option('--list-instances', is_flag=True, help='List EC2 instances.')
@click.option('--start-instance', type=str, help='Start an EC2 instance (provide instance_id).')
@click.option('--stop-instance', type=str, help='Stop an EC2 instance (provide instance_id).')
def main(set_default, set_region, list_buckets_option, upload_file, download_file, list_instances, start_instance, stop_instance):
    """ Main function for CLI tool. """
    profile = get_default_profile()

    # בדוק את ה-SSO Token וחדש אותו במידת הצורך
    ensure_sso_token(profile)

    # כעת המשך לשאר הפקודות
    region = get_default_region()
    if not region or set_region:
        region = choose_region()

    if set_default:
        click.echo(f"Default profile is set to {profile}")
    elif list_buckets_option:
        list_s3_buckets(profile, region)  # כאן נקרא לפונקציה האמיתית
    elif upload_file:
        file_path, bucket_name = upload_file
        upload_file(profile, file_path, bucket_name, region)
    elif download_file:
        bucket_name, object_name, file_path = download_file
        download_file(profile, bucket_name, object_name, file_path, region)
    elif list_instances:
        list_instances(profile, region)
    elif start_instance:
        start_instance(profile, start_instance, region)
    elif stop_instance:
        stop_instance(profile, stop_instance, region)
    else:
        verify_identity(profile, region)

if __name__ == "__main__":
    main()
