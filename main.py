import boto3
import subprocess
import json
from botocore.exceptions import ClientError
from models import Aws_Validation, exec_file_as_json, list_instances, list_alb, run_terraform_run_python_script, run_terraform

# # AWS Region
# REGION = "us-east-1"

# # Terraform output values (replace these with actual Terraform outputs)
# INSTANCE_ID = "i-0ebd8ab2e1a0cc6f5"  # Replace with your instance ID from Terraform
# ALB_NAME = "my-alb"  # Replace with your ALB name

run_terraform_run_python_script()
run_terraform()


instance_details = list_instances(INSTANCE_ID)
alb_details = list_alb(ALB_NAME)
final_defails = {**instance_details, **alb_details} #merge the two dictionaries
exec_file_as_json(Aws_Validation(**final_defails), "aws_validation.json")
