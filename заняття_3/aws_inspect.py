import boto3
import pprint

session = boto3.Session(region_name='us-east-1', profile_name='default')

identity = session.client('sts').get_caller_identity()
print(identity)

iam = session.client('iam')
users = iam.list_users()
groups = iam.list_groups()

user_names = [user['UserName'] for user in users['Users']]
print("IAM users: ", user_names)

group_names = [group['GroupName'] for group in groups['Groups']]
print("IAM groups: ", group_names)

s3_support_group = iam.get_group(GroupName='S3-Support')
members = [user['UserName'] for user in s3_support_group['Users']]
print("S3-Support group members: ", members)

# iam.add_user_to_group(UserName='user-1', GroupName='S3-Support')
#print("user-1 has been added to S3-Support group.")

# iam.remove_user_from_group(UserName='user-1', GroupName='S3-Support')
# print("user-1 has been removed from S3-Support group.")

attached = iam.list_attached_group_policies(GroupName='S3-Support')['AttachedPolicies']
print(attached)
policy_arn = attached[0]['PolicyArn']

policy = iam.get_policy(PolicyArn=policy_arn)['Policy']
pprint.pprint(policy)

document = iam.get_policy_version(PolicyArn=policy_arn, VersionId=policy['DefaultVersionId'])['PolicyVersion']
pprint.pprint(document)

# AWS S3
s3 = session.client('s3')
buckets = s3.list_buckets()['Buckets']
print(buckets)

# AWS EC2
ec2 = boto3.client('ec2')
instances = ec2.describe_instances()
print(instances)