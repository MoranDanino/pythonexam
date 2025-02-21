provider "aws" {
 region = "us-east-1"
}

resource "aws_instance" "web_server" {
 ami = "ami-0dee1ac7107ae9f8c"
 instance_type = "t4g.small"
 availability_zone = "us-east-1a"
 subnet_id = aws_subnet.public[0].id  ###add subnet to the instance
 tags = {
   Name = "WebServer"
 }
}

resource "aws_lb" "application_lb" {
 name = "my-lb"
 internal = false
 load_balancer_type = "application"
 security_groups = [aws_security_group.lb_sg.id]
 subnets = [for subnet in aws_subnet.public : subnet.id] #change
}

resource "aws_security_group" "lb_sg" {
 name        = "lb_security_group"
 #add vpc reference
 vpc_id      = aws_vpc.main.id   # reference to the VPC created below
 description = "Allow HTTP inbound traffic"

 ingress {
   from_port   = 80
   to_port     = 80
   protocol    = "tcp"
   cidr_blocks = ["0.0.0.0/0"]
 }
 #add outbound rule
 egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_lb_listener" "http_listener" {
 load_balancer_arn = aws_lb.application_lb.arn
 port              = 80
 protocol          = "HTTP"

 default_action {
   type             = "forward"
   target_group_arn = aws_lb_target_group.web_target_group.arn
 }
}

resource "aws_lb_target_group" "web_target_group" {
 name     = "web-target-group"
 port     = 80
 protocol = "HTTP"
 vpc_id   = aws_vpc.main.id
}

resource "aws_lb_target_group_attachment" "web_instance_attachment" {
 target_group_arn = aws_lb_target_group.web_target_group.arn
 target_id        = aws_instance.web_server.id
 port             = 80  #add port
}

resource "aws_subnet" "public" {
 count = 2
 vpc_id = aws_vpc.main.id
 cidr_block = "10.0.${count.index}.0/24"
 availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
 map_public_ip_on_launch = true   #add this line to enable public IP
}

resource "aws_vpc" "main" {
 cidr_block = "10.0.0.0/16"
}

####adding internet gateway - did not work in my account without it, remind task 4 in terraform exam####
resource "aws_internet_gateway" "gateway" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public_route" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route" "internet_access" {
  route_table_id = aws_route_table.public_route.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.gateway.id
}

resource "aws_route_table_association" "public_assoc" {
  count = length(aws_subnet.public[*].id)
  route_table_id = aws_route_table.public_route.id
  subnet_id = aws_subnet.public[count.index].id
}

#### outputs:
output "instance_id" {
  value = aws_instance.web_server.id
}

output "lb_dns_name" {
    value = aws_lb.application_lb.dns_name
}
