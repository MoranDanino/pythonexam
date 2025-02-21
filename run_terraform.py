from jinja2 import Template, Environment, FileSystemLoader
import os

#create a jinja2 environment
env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))))
template = env.get_template("templateJ.j2")


#dictionary to store the possible AMI
ami_dict = {"ubuntu": "ami-0dee1ac7107ae9f8c", 
       "amazon linux": "ami-0f1a6835595fb9246"}
#list to store the possible instance types
instance_type_dict = {"small": "t3.small",
                  "medium": "t3.medium"}
region_dict = {"us-east-1": "us-east-1"}
#list to store the possible availability zones
availability_zone_dict = {"az1":"us-east-1a", 
                     "az2":"us-east-1b", 
                     "az3":"us-east-1c", 
                     "az4":"us-east-1d", 
                     "az5":"us-east-1e"}

#list to store the default load balancer name
load_balancer_dict = {"default_name": "myloadbalancer"}


print("Hello user, please enter the following information: ")
ami = input("Enter the AMI type: (options: ubuntu or amazon linux) ").strip().lower()
instance_type = input("Enter your instance type: (options: small or medium) ").strip().lower()
region = input("Enter your region: (allows only: us-east-1)").strip().lower()
az = input("Enter your availability zone: (allows only exit az: az1-az6)").strip().lower()
lb = input("Enter your load balancer name: ")  
if lb == "" or lb == " ":
    lb = "myloadbalancer"  #default load balancer name

#check if the user input is valid, if not, use the default value
ami = ami_dict.get(ami, "ami-?????")
instance_type = instance_type_dict.get(instance_type, "t3.small")
region = region_dict.get(region, "us-east-1")
az = availability_zone_dict.get(az, "us-east-1a")

#use help from gpt
vars = template.render(
    ami = ami,
    instance_type = instance_type,
    region = region,
    availability_zone = az,
    load_balancer_name = lb
    )

#open the file and write the rendered template to it
with open("myterraform.tf", "w") as f:
    f.write(vars)
