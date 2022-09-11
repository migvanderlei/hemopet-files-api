import os
import boto3

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


class S3Client:

    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.s3 = self.session.client("s3")

    def upload(self, file, key, bucket='pet-files'):
        self.s3.upload_fileobj(
            file,
            bucket,
            key,
        )

    def download(self, key, bucket='pet-files'):
        try:
            response = self.s3.get_object(
                Bucket=bucket,
                Key=key,
            )
        
            return response['Body'].read()
        except:
            return None

    def remove(self, key, bucket='pet-files'):
        self.s3.delete_object(
            Bucket=bucket,
            Key=key
        )
