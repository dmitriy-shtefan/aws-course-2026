import boto3


def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "original_s3_uri": "",
        "thumbnail_s3_uri": "",
    }