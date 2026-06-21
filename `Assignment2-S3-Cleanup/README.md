# Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

## Objective
Automatically delete files older than 30 days from an S3 bucket using AWS Lambda.

---

## Steps Followed

### Step 1: Create S3 Bucket
- Navigate to **Services → S3 → Create bucket**.
- Configure:
  - Bucket name: `cleanup-demo-bucket-hvassignment.
  - Region: Your preferred region.
  - Keep other defaults.

---

### Step 2: Upload Test Files
- Open your newly created bucket.
- Click **Upload** → add several files (images, text files, etc.).

> 💡 For testing, i have temporarily set the threshold to 1 minute instead of 30 days, since you can’t easily upload files older than 30 days.

---

### Step 3: Create IAM Role for Lambda
- Navigate to **IAM → Roles → Create role**.
- Select AWS service → Lambda.
- Attach policy: **AmazonS3FullAccess**.
- Role name: `Lambda-S3-Cleanup-Role`.
---

### Step 4: Create Lambda Function
- Navigate to **Lambda → Create function**.
- Function name: `S3-Bucket-Cleanup`.
- Runtime: Python 3.12.
- Execution role: Use existing → `Lambda-S3-Cleanup-Role`.

---

### Step 5: Write the Lambda Code
```python
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
```
### Step 6: Increase Timeout
  - Go to Configuration → General configuration → Edit.
  - Set Timeout: 1 minute.

### Step 7: Test the Function
  - Click Test → Create test event → Event JSON: {} → Save → Test.
  - Check execution results for deleted files.

### Step 8: Verify in S3
  - Navigate to your S3 bucket.
  - Confirm old files are deleted.

### Methods Used
  - AWS Lambda for automation.
  - Boto3 SDK for S3 operations (list_objects_v2, delete_object).
  - IAM Role with AmazonS3FullAccess policy.
  - Datetime comparison to calculate file age.

### Results
Lambda successfully deleted files older than 30 days (or shorter threshold for testing).

Verified cleanup in S3 bucket dashboard.
