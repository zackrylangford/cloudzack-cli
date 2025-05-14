#!/usr/bin/env python3

import boto3
import argparse
import sys
from botocore.exceptions import ClientError

def list_instances(ec2_client, filters=None):
    """List EC2 instances with their IDs, names, states, and IP addresses"""
    try:
        if filters:
            response = ec2_client.describe_instances(Filters=filters)
        else:
            response = ec2_client.describe_instances()
        
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_state = instance['State']['Name']
                instance_name = "Unnamed"
                public_ip = instance.get('PublicIpAddress', 'None')
                
                # Get the Name tag if it exists
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            instance_name = tag['Value']
                            break
                
                instances.append({
                    'id': instance_id,
                    'name': instance_name,
                    'state': instance_state,
                    'public_ip': public_ip
                })
        
        return instances
    except ClientError as e:
        print(f"Error listing instances: {e}")
        sys.exit(1)

def start_instance(ec2_client, instance_id):
    """Start an EC2 instance by ID"""
    try:
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        print(f"Starting instance {instance_id}...")
        return response
    except ClientError as e:
        print(f"Error starting instance {instance_id}: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Start an AWS EC2 instance')
    parser.add_argument('--id', help='Instance ID to start')
    parser.add_argument('--name', help='Instance name to start')
    parser.add_argument('--region', default='us-east-1', help='AWS region (default: us-east-1)')
    parser.add_argument('--list', action='store_true', help='List available instances')
    args = parser.parse_args()
    
    # Initialize the EC2 client
    ec2_client = boto3.client('ec2', region_name=args.region)
    
    # List instances if requested
    if args.list:
        instances = list_instances(ec2_client)
        print("\nAvailable instances:")
        print(f"{'ID':<20} {'Name':<30} {'State':<10} {'Public IP':<15}")
        print("-" * 75)
        for instance in instances:
            print(f"{instance['id']:<20} {instance['name']:<30} {instance['state']:<10} {instance['public_ip']:<15}")
        return
    
    # Start by name if provided
    if args.name:
        filters = [{'Name': 'tag:Name', 'Values': [args.name]}]
        instances = list_instances(ec2_client, filters)
        
        if not instances:
            print(f"No instance found with name: {args.name}")
            sys.exit(1)
        
        if len(instances) > 1:
            print(f"Multiple instances found with name: {args.name}")
            print(f"{'ID':<20} {'Name':<30} {'State':<10} {'Public IP':<15}")
            print("-" * 75)
            for instance in instances:
                print(f"{instance['id']:<20} {instance['name']:<30} {instance['state']:<10} {instance['public_ip']:<15}")
            sys.exit(1)
        
        instance_id = instances[0]['id']
        print(f"Found instance: {instances[0]['name']} ({instance_id})")
        
    # Use instance ID if provided
    elif args.id:
        instance_id = args.id
    else:
        parser.print_help()
        print("\nError: You must specify either --id or --name")
        sys.exit(1)
    
    # Start the instance
    start_instance(ec2_client, instance_id)
    
    # Check the status
    print("Waiting for instance to start...")
    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    
    # Get the public IP address
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]
    public_ip = instance.get('PublicIpAddress', 'None')
    
    print(f"Instance {instance_id} is now running")
    print(f"Public IP address: {public_ip}")
    if public_ip != 'None':
        print(f"SSH command: ssh ec2-user@{public_ip}")
        print("Note: The username might be different based on your AMI (e.g., ubuntu, ec2-user, admin)")

if __name__ == "__main__":
    main()