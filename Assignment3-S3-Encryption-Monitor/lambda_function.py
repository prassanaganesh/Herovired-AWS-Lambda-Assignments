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
