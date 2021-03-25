import logging

import boto3
from botocore.exceptions import ClientError


class Importer:
    REGION = 'eu-central-1'
    BUCKET = 'qymatix-accounts-eu-central-1'

    def __init__(self, account_name):
        self.s3_client = boto3.client('s3', region_name=self.REGION)
        self.account_name = account_name

    def create_bucket(self, bucket_name, region=REGION):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """

        # Create bucket
        try:
            location = {'LocationConstraint': region}
            self.s3_client.create_bucket(Bucket=bucket_name,
                                         CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def list_buckets(self):
        # Retrieve the list of existing buckets
        response = self.s3_client.list_buckets()

        # Output the bucket names
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')

    def upload_file(self, file_name, bucket=BUCKET, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = self.account_name + '/' + file_name.split('/')[-1]

        # Upload the file
        try:
            response = self.s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True
