import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Configuration
    bucket_name = 'cleanup-demo-bucket-hvassignment
    days_threshold = 30  # Files older than this will be deleted
    
    # Calculate cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_threshold)
    
    deleted_files = []
    
    # List all objects in the bucket
    paginator = s3.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=bucket_name):
        if 'Contents' not in page:
            print("Bucket is empty")
            continue
            
        for obj in page['Contents']:
            last_modified = obj['LastModified']
            
            if last_modified < cutoff_date:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                deleted_files.append(obj['Key'])
                print(f"Deleted: {obj['Key']} (Last modified: {last_modified})")
    
    print(f"Total files deleted: {len(deleted_files)}")
    
    return {
        'statusCode': 200,
        'body': {
            'deleted_count': len(deleted_files),
            'deleted_files': deleted_files
        }
    }
