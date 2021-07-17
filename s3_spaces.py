import boto3
from config import AWS_S3_ENDPOINT_URL, AWS_S3_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, \
    AWS_STORAGE_BUCKET_NAME


class S3DigitalOceanSpace:

    def __init__(self, reg_name, endpoint, key, access_key, bucket):
        session = boto3.session.Session()
        self.bucket = bucket
        self.client = session.client('s3',
                                     region_name=reg_name,
                                     endpoint_url=endpoint,
                                     aws_access_key_id=key,
                                     aws_secret_access_key=access_key)

    def upload_file(self, file_name, content):
        return self.client.put_object(Bucket=self.bucket, Key=file_name, Body=content, ACL='private')

    def list_files(self):
        _list = self.client.list_objects(Bucket=self.bucket)['Contents']
        _list.sort(key=lambda x: x['LastModified'])
        return _list

    def download_file(self, file_name, path_to_file='/tmp'):
        return self.client.download_file(self.bucket, file_name, f'{path_to_file}/{file_name}')

    def delete_file(self, file_name):
        return self.client.delete_object(Bucket=self.bucket, Key=file_name)


s3_space = S3DigitalOceanSpace(AWS_S3_REGION_NAME,
                               AWS_S3_ENDPOINT_URL,
                               AWS_ACCESS_KEY_ID,
                               AWS_SECRET_ACCESS_KEY,
                               AWS_STORAGE_BUCKET_NAME)
