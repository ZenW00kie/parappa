import boto3
from boto3.s3.transfer import S3Transfer
import os

class BotoClient:

    def __init__(self, filename, bucket_name):
        s3 = boto3.client('s3')
        self.transfer = S3Transfer(s3)
        self.__s3_connect(filename, bucket_name)

############################# PRIVATE FUNCTIONS  ###############################

    def __s3_connect(self, filename, bucket_name):
        self.transfer.upload_file(filename,
                            bucket_name,
                            filename
                           )
        os.remove(filename)
