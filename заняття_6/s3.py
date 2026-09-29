import boto3
import pprint


bucket = input("Введіть імʼя бакету:")

s3 = boto3.client('s3', region_name='us-east-1')

response = s3.list_objects_v2(Bucket=bucket)
pprint.pprint(response['Contents'])

s3.upload_file('static-site-policy.json', bucket, 'static-site-policy-2.json')

s3.download_file(bucket, 'index.html', 'site-index.html')