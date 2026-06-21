import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Find and stop instances with Auto-Stop tag
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
    else:
        print("No running instances with Auto-Stop tag found")
    
    # Find and start instances with Auto-Start tag
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
    else:
        print("No stopped instances with Auto-Start tag found")
    
    return {
        'statusCode': 200,
        'body': {
            'stopped': stop_instance_ids,
            'started': start_instance_ids
        }
    }
