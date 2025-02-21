import boto3
import os

s3_client = boto3.client("s3")

def handler(event, context):
    bucket_name = os.environ["BUCKET_NAME"]
    file_name = os.environ["FILE_NAME"]

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        file_content = response["Body"].read().decode("utf-8")
        return {
            "statusCode": 200,
            "body": file_content
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error reading file: {str(e)}"
        }