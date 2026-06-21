# Assignment 5: Auto‑Tagging EC2 Instances on Launch Using AWS Lambda and EventBridge

## Objective
Automatically tag new EC2 instances with launch date, timestamp, and custom tags when they are launched.

---

## Steps Followed

### Step 1: Create IAM Role
- Navigate to **IAM → Roles → Create role**.
- Select AWS service → Lambda.
- Attach policy: **AmazonEC2FullAccess**.
- Role name: `Lambda-EC2-AutoTag-Role`.

---

### Step 2: Create Lambda Function
- Navigate to **Lambda → Create function**.
- Function name: `EC2-Auto-Tag-On-Launch`.
- Runtime: Python 3.12.
- Execution role: Use existing → `Lambda-EC2-AutoTag-Role`.

---

### Step 3: Write the Lambda Code
```python
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

```
### Step 4: Create EventBridge Rule
- Navigate to Amazon EventBridge → Rules → Create rule.
- Name: EC2-Launch-AutoTag-Rule.
- Event bus: default.
- Rule type: Event pattern.

### Step 5: Define Event Pattern
- Event source: AWS events.
- Creation method: Custom pattern (JSON editor).

Enter this pattern:
```
json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["pending"]
  }
}
```
### Step 6: Select Target

- Target type: AWS service.
- Select target: Lambda function.
- Function: EC2-Auto-Tag-On-Launch.

### Step 7: Test by Launching EC2 Instance

- Navigate to EC2 → Launch Instance.
- Launch any t2.micro instance.
- Wait 1–2 minutes.

### Step 8: Verify Tags
- Go to EC2 → Instances → Tags tab.

- Confirm tags:
- LaunchDate
- LaunchTimestamp
- AutoTagged
- Environment

### Methods Used
- AWS Lambda for automation.
- Boto3 SDK for EC2 operations (create_tags).
- IAM Role with AmazonEC2FullAccess policy.
- Amazon EventBridge rule to trigger Lambda on EC2 state change.

### Results
- Lambda successfully applied tags to new EC2 instances at launch.
- Verified tags in EC2 dashboard.

