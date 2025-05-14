#!/usr/bin/env python3

import boto3
import argparse
import sys
from botocore.exceptions import ClientError

def list_instances(ec2_client, filters=None):
    """List EC2 instances with their IDs, names, and states"""
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
                
                # Get the Name tag if it exists
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            instance_name = tag['Value']
                            break
                
                instances.append({
                    'id': instance_id,
                    'name': instance_name,
                    'state': instance_state
                })
        
        return instances
    except ClientError as e:
        print(f"Error listing instances: {e}")
        sys.exit(1)

def stop_instance(ec2_client, instance_id):
    """Stop an EC2 instance by ID"""
    try:
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        print(f"Stopping instance {instance_id}...")
        return response
    except ClientError as e:
        print(f"Error stopping instance {instance_id}: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Stop an AWS EC2 instance')
    parser.add_argument('--id', help='Instance ID to stop')
    parser.add_argument('--name', help='Instance name to stop')
    parser.add_argument('--region', default='us-east-1', help='AWS region (default: us-east-1)')
    parser.add_argument('--list', action='store_true', help='List available instances')
    parser.add_argument('--force', action='store_true', help='Force stop the instance')
    args = parser.parse_args()
    
    # Initialize the EC2 client
    ec2_client = boto3.client('ec2', region_name=args.region)
    
    # List instances if requested
    if args.list:
        instances = list_instances(ec2_client)
        print("\nAvailable instances:")
        print(f"{'ID':<20} {'Name':<30} {'State':<10}")
        print("-" * 60)
        for instance in instances:
            print(f"{instance['id']:<20} {instance['name']:<30} {instance['state']:<10}")
        return
    
    # Stop by name if provided
    if args.name:
        filters = [{'Name': 'tag:Name', 'Values': [args.name]}]
        instances = list_instances(ec2_client, filters)
        
        if not instances:
            print(f"No instance found with name: {args.name}")
            sys.exit(1)
        
        if len(instances) > 1:
            print(f"Multiple instances found with name: {args.name}")
            print(f"{'ID':<20} {'Name':<30} {'State':<10}")
            print("-" * 60)
            for instance in instances:
                print(f"{instance['id']:<20} {instance['name']:<30} {instance['state']:<10}")
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
    
    # Stop the instance
    stop_instance(ec2_client, instance_id)
    
    # Check the status
    print("Waiting for instance to stop...")
    waiter = ec2_client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance_id])
    print(f"Instance {instance_id} is now stopped")

if __name__ == "__main__":
    main()