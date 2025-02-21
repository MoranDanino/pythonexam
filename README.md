# files: 

main.py : Should automatically execute the scripts to return a JSON file with the required values -> it works if i give manually the instance_id and the lb_dns_name
models.py : functions and classes
run_terraform.py : run the jinja2 template and output valid gerraform file. 
            -> myterraform.tf: I have few error in the mission and check my terraform file on my aws account: works and return 
            Outputs:

            instance_id = "i-0f70f27f73ce46035"
            lb_dns_name = "my-lb-1914586692.us-east-1.elb.amazonaws.com" 

            in my case. 


            -> terraform output -json   : return: 
            {
            "instance_id": {
                "sensitive": false,
                "type": "string",
                "value": "i-0f70f27f73ce46035"
            },
            "lb_dns_name": {
                "sensitive": false,
                "type": "string",
                "value": "my-lb-1914586692.us-east-1.elb.amazonaws.com"
            }
            }
            as needed. 
            
            *Due to lack of time, I was unable to integrate everything and run the scripts automatically. 
templateJ.j2 : template for the terraform file
requirements : the packages I need to install for the mission 
#


how to run: 
first run manually run_terraform.py and get the terraform file
then the terraform file: myterraform.tf 
and then the main with the output of the terraform file
