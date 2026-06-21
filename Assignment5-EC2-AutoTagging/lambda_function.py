import boto3
import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Extract instance ID from the event
    instance_id = event['detail']['instance-id']
    
    # Create tags: current date + custom tag
    tags = [
        {'Key': 'LaunchDate', 'Value': datetime.datetime.now().strftime("%Y-%m-%d")},
        {'Key': 'Owner', 'Value': 'AutoTagLambda'}
    ]
    
    # Apply tags
    ec2.create_tags(Resources=[instance_id], Tags=tags)
    
    print(f"Tagged instance {instance_id} with {tags}")
