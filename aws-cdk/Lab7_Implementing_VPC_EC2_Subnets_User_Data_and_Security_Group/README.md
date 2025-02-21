# Lab 7: Implementing VPC, EC2, Subnets, User Data, and Security Group using AWS CDK

## Objective
The objective of this lab is to demonstrate how to set up a Virtual Private Cloud (VPC), launch an EC2 instance in a subnet, configure user data, and create a security group using AWS CDK in Python. By completing this lab, participants will understand how to manage networking and compute resources programmatically.

## Prerequisites
- AWS account
- AWS CLI installed and configured
- Node.js installed
- AWS CDK installed (`npm install -g aws-cdk`)
- Python installed (recommended: Python 3.8 or later)
- An IDE such as VSCode

## Steps

### Step 1: Setup Project Directory
1. Create a new folder for the project and navigate into it:
   ```sh
   mkdir vpc-ec2-cdk-lab
   cd vpc-ec2-cdk-lab
   ```
2. Open the folder in VSCode:
   ```sh
   code .
   ```
3. Open the terminal in VSCode.

### Step 2: Initialize CDK App
1. Initialize a new AWS CDK app in Python:
   ```sh
   cdk init app --language python
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install AWS CDK dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Step 3: Define VPC, EC2, Subnets, User Data, and Security Group
1. Open `vpc_ec2_cdk_lab/vpc_ec2_cdk_lab_stack.py` and modify it as follows:
```python
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2

class VpcEc2CdkLabStack(core.Stack):
      def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
           super().__init__(scope, id, **kwargs)

           # Create VPC
           vpc = ec2.Vpc(
               self, "MyVPC",
               max_azs=2,
               subnet_configuration=[
                   ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC),
                   ec2.SubnetConfiguration(name="Private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
               ]
           )

           # Create Security Group
           security_group = ec2.SecurityGroup(
               self, "MySecurityGroup",
               vpc=vpc,
               description="Allow SSH access",
               allow_all_outbound=True
           )
           security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH access")

           # User Data for EC2 Instance
           user_data = ec2.UserData.for_linux()
           user_data.add_commands(
               "#!/bin/bash",
               "yum update -y",
               "yum install -y httpd",
               "systemctl start httpd",
               "systemctl enable httpd"
           )

           # Create EC2 Instance
           ec2_instance = ec2.Instance(
               self, "MyEC2Instance",
               instance_type=ec2.InstanceType("t2.micro"),
               machine_image=ec2.AmazonLinuxImage(),
               vpc=vpc,
               security_group=security_group,
               user_data=user_data
           )
 
```

### Step 4: Bootstrap and Deploy
1. Bootstrap the AWS environment (only required once per AWS account/region):
   ```sh
   cdk bootstrap
   ```
2. Synthesize the CloudFormation template:
   ```sh
   cdk synth
   ```
3. Deploy the stack:
   ```sh
   cdk deploy
   ```

### Step 5: Verify Deployment
1. Go to the AWS EC2 Console.
2. Verify that the EC2 instance is running inside the VPC with the specified security group.
3. Connect to the EC2 instance via SSH to check that the user data script has run successfully.

### Step 6: Cleanup
1. To remove all AWS resources created, run:
   ```sh
   cdk destroy
   ```

## Conclusion
✅ Created a **VPC** with public and private subnets  
✅ Configured an **EC2 instance** inside the VPC  
✅ Defined a **Security Group** to allow SSH access  
✅ Used **User Data** to install and start a web server  
✅ Deployed everything using **AWS CDK**  

You now have a **networked EC2 instance** provisioned using Infrastructure as Code! 🚀

