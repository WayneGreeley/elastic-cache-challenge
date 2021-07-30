import os
import cfnresponse
import boto3


def lambda_handler(event, context):
    try:
        
        string = "some-string"
        encoded_string = string.encode("utf-8")
    
        bucket_name = "lambda-artifacts-bef726211f8f0d84"
        file_name = "hello.txt"
        s3_path = "s3_path/" + file_name
    
        s3 = boto3.resource("s3")
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except (Exception) as error:
        print(error)
        cfnresponse.send(event, context, cfnresponse.FAILED, {})
