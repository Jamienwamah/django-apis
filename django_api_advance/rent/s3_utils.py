# s3_utils.py

import boto3
from botocore.exceptions import NoCredentialsError
from decouple import config

def upload_to_s3(local_file_path, s3_key):
    aws_access_key_id = config('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = config('AWS_SECRET_ACCESS_KEY')
    aws_storage_bucket_name = config('AWS_STORAGE_BUCKET_NAME')

    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    try:
        s3.upload_file(local_file_path, aws_storage_bucket_name, s3_key)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
