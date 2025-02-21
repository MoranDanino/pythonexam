import json
from dataclasses import dataclass
import boto3
from botocore.exceptions import ClientError
import subprocess

#dataclass to store the details we need
@dataclass
class Aws_Validation:
    instance_id: str
    instance_state: str
    public_ip: str
    load_balancer_dns: str


#this works manually, not automatically
def get_terraform_output(output_name):
    result = subprocess.run(["terraform", "output", "-json"], capture_output=True, text=True)
    try:
        outputs = json.loads(result.stdout)
        return outputs.get(output_name, {}).get("value")
    except json.JSONDecodeError:
        print("Error: problem with terraform output")
        return None



def list_instances(INSTANCE_ID):
    details = {}
    ec2_client = boto3.client("ec2")
    try:
        response = ec2_client.describe_instances(InstanceIds=[INSTANCE_ID])
        for res in response["Reservations"]:
            for instance in res["Instances"]:
                details["instance_id"] = instance["InstanceId"]
                details["instance_state"] = instance["State"]["Name"]
                details["public_ip"] = instance.get("PublicIpAddress", "N/A")
        return details
    except ClientError as e:
        if "InvalidInstanceID" in str(e):
            print ("instance_id: invalid Instance ID")
        if "AccessDenied" in str(e):
            print ("load_balancer_dns: access Denied")
        exit()

def list_alb(ALB_NAME):
    details = {}
    elb_client = boto3.client("elbv2", region_name="us-east-1")
    try:
        response = elb_client.describe_load_balancers(Names=[ALB_NAME])
        for lb in response["LoadBalancers"]:
            details["load_balancer_dns"] = lb["DNSName"]
        return details
    except ClientError as e:
        if "LoadBalancerNotFound" in str(e):
            print ("load_balancer_dns: not found")
        if "AccessDenied" in str(e):
            print ("load_balancer_dns : access Denied")
        exit()


#write the details we need to a file as json
def exec_file_as_json(data: Aws_Validation, file_name: str):
    with open(file_name, "w") as file:
        json.dump(data.__dict__, file, indent=4)  #convert the dataclass to json and write it to the file
