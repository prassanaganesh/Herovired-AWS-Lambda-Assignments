# Assignment 1: Automated Instance Management Using AWS Lambda and Boto3

## Objective
Automatically stop/start EC2 instances based on tags (`Action=Auto-Stop` and `Action=Auto-Start`).

## Steps Followed

### Step 1: Create Two EC2 Instances
- Sign in to the AWS Management Console.
- Navigate to **Services → EC2 → Launch Instance**.
- Configure the first instance:
  - Name: `Auto-Stop-Instance`
  - AMI: Amazon Linux 2023 (free-tier eligible)
  - Instance type: `t2.micro`
  - Key pair: Create new or select existing
  - Network settings: Default VPC, allow SSH
- Launch the instance.
- Repeat for the second instance:
  - Name: `Auto-Start-Instance`
  - Same configuration as above.

---

### Step 2: Tag the Instances
- Select `Auto-Stop-Instance` → Actions → Instance settings → Manage tags.
- Add tag: **Key = Action, Value = Auto-Stop**.
- Select `Auto-Start-Instance` → Add tag: **Key = Action, Value = Auto-Start**.

---

### Step 3: Prepare Instance States for Testing
- Stop the `Auto-Start-Instance`.
- Keep `Auto-Stop-Instance` running.

---

### Step 4: Create IAM Role for Lambda
- Navigate to **IAM → Roles → Create role**.
- Select AWS service → Lambda.
- Attach policy: **AmazonEC2FullAccess**.
- Name: `Lambda-EC2-Management-Role`.
---

### Step 5: Create the Lambda Function
- Navigate to **Lambda → Create function**.
- Function name: `EC2-Auto-Manage`.
- Runtime: Python 3.12.
- Architecture: x86_64.
- Execution role: Use existing → `Lambda-EC2-Management-Role`.
---

### Step 6: Write the Lambda Code

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Stop instances with Auto-Stop tag
    auto_stop_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Stop']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    stop_instance_ids = []
    for reservation in auto_stop_instances['Reservations']:
        for instance in reservation['Instances']:
            stop_instance_ids.append(instance['InstanceId'])
    if stop_instance_ids:
        ec2.stop_instances(InstanceIds=stop_instance_ids)
        print(f"Stopped instances: {stop_instance_ids}")
    
    # Start instances with Auto-Start tag
    auto_start_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Start']},
            {'Name': 'instance-state-name', 'Values': ['stopped']}
        ]
    )
    start_instance_ids = []
    for reservation in auto_start_instances['Reservations']:
        for instance in reservation['Instances']:
            start_instance_ids.append(instance['InstanceId'])
    if start_instance_ids:
        ec2.start_instances(InstanceIds=start_instance_ids)
        print(f"Started instances: {start_instance_ids}")
    
    return {
        'statusCode': 200,
        'body': {
            'stopped': stop_instance_ids,
            'started': start_instance_ids
        }
    }

```
---
### Step 7: Configure Timeout
  - Go to Configuration → General configuration → Edit.
  - Set Timeout: 30 seconds.

---
### Step 8: Test the Lambda Function
  - Click Test → Create test event → Event JSON: {} → Save → Test.
  - Check execution results for success message.
---
### Step 9: Verify in EC2 Dashboard
  - Refresh EC2 dashboard.
  - Confirm:
    Auto-Stop-Instance is now stopped.
    Auto-Start-Instance is now running.
---
### Methods Used
  - AWS Lambda for automation.
  - Boto3 SDK for EC2 operations (describe_instances, stop_instances, start_instances).
  - IAM Role with AmazonEC2FullAccess policy.
  - Tags (Action=Auto-Stop, Action=Auto-Start) to identify instances
---    .
### Results
  - Lambda successfully stopped the running instance with Auto-Stop tag.
  - Lambda successfully started the stopped instance with Auto-Start tag.
  - Automation verified in EC2 dashboard.


