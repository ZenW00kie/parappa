import boto3
from boto3.s3.transfer import S3Transfer
import os

class BotoClient:

    def __init__(self):
        s3 = boto3.client('s3')
        transfer = S3Transfer(s3)
        s3_connect(filename, bucket_name)

############################# PRIVATE FUNCTIONS  ###############################

    def __s3_connect(self, filename, bucket_name):
        transfer.upload_file(filename,
                            bucket_name,
                            filename
                           )
        os.remove(filename)
        os.remove('apwide.csv')
