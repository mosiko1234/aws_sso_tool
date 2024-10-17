def main(set_default, set_region, list_buckets_option, upload_file, download_file, list_instances, start_instance, stop_instance):
    """ Main function for CLI tool. """
    try:
        profile = get_default_profile()
        if not profile:
            click.echo("Error: No default profile found. Please set one using --set-default.")
            return

        # בדוק את ה-SSO Token וחדש אותו במידת הצורך
        ensure_sso_token(profile)

        # כעת המשך לשאר הפקודות
        region = get_default_region()
        if not region or set_region:
            region = choose_region()

        if list_buckets_option:
            list_s3_buckets(profile, region)
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
    except Exception as e:
        click.echo(f"An error occurred: {e}")
