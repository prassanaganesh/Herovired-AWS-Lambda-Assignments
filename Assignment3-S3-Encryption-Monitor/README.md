# Assignment 3: Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3

## Objective
Detect S3 buckets without server-side encryption and log them for review.

---

## Steps Followed

### Step 1: Create Test Buckets
- Navigate to **Services → S3 → Create bucket**.
- Create **Bucket 1 (encrypted)**:
  - Name: `encrypted-test-bucket-[unique-id]`
  - Under Default encryption: Enable Server-side encryption → Choose SSE-S3.
- Create **Bucket 2 (unencrypted)**:
  - Name: `unencrypted-test-bucket-[unique-id]`
  - Under Default encryption: Disable or skip encryption.
---

### Step 2: Create IAM Role
- Navigate to **IAM → Roles → Create role**.
- Select AWS service → Lambda.
- Attach policy: **AmazonS3ReadOnlyAccess**.
- Role name: `Lambda-S3-Encryption-Audit-Role`.

---

### Step 3: Create Lambda Function
- Navigate to **Lambda → Create function**.
- Function name: `S3-Encryption-Monitor`.
- Runtime: Python 3.12.
- Execution role: Use existing → `Lambda-S3-Encryption-Audit-Role`.
---

### Step 4: Write the Lambda Code
```python
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Get all buckets
    response = s3.list_buckets()
    
    unencrypted_buckets = []
    encrypted_buckets = []
    
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        
        try:
            # Try to get bucket encryption configuration
            encryption = s3.get_bucket_encryption(Bucket=bucket_name)
            encrypted_buckets.append(bucket_name)
            print(f"✓ ENCRYPTED: {bucket_name}")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                unencrypted_buckets.append(bucket_name)
                print(f"✗ UNENCRYPTED: {bucket_name}")
            else:
                print(f"? ERROR checking {bucket_name}: {error_code}")
    
    print("\n" + "="*50)
    print(f"Total buckets: {len(response['Buckets'])}")
    print(f"Encrypted: {len(encrypted_buckets)}")
    print(f"Unencrypted: {len(unencrypted_buckets)}")
    print("="*50)
    
    if unencrypted_buckets:
        print("\n⚠️ ACTION REQUIRED - Unencrypted buckets:")
        for bucket in unencrypted_buckets:
            print(f"  - {bucket}")
    
    return {
        'statusCode': 200,
        'body': {
            'unencrypted_buckets': unencrypted_buckets,
            'encrypted_buckets': encrypted_buckets
        }
    }
```

### Step 5: Test and Review Logs
  - Click Test → Run with empty event {}.
  - Check execution results.
  - Navigate to Monitor → View CloudWatch logs for detailed output.

### Methods Used
AWS Lambda for automation.

  - Boto3 SDK for S3 operations (list_buckets, get_bucket_encryption).
  - IAM Role with AmazonS3ReadOnlyAccess policy.
  - Exception handling to detect unencrypted buckets.

### Results
  - Lambda successfully identified encrypted and unencrypted buckets.
  - Logs clearly show which buckets require encryption.
  - Verified results in CloudWatch logs.



