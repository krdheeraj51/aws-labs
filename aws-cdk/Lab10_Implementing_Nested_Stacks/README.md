# **Lab 10: Implementing Nested Stacks in AWS CDK**  

## **Objective**  
The goal of this lab is to demonstrate **Nested Stacks in AWS CDK**. Nested stacks allow you to break down complex infrastructures into smaller, manageable stacks while keeping them logically connected.  

In this lab, we will create:  
1. **A Root Stack (MainStack)** that includes:  
   - **A Nested VPC Stack (NetworkStack)** to create a VPC  
   - **A Nested EC2 Stack (ComputeStack)** that launches an EC2 instance inside the VPC  

By the end of this lab, you will understand how **nested stacks** work in AWS CDK and how they help maintain modular infrastructure as code (IaC).  

---

## **Prerequisites**  
- AWS account with IAM access  
- AWS CLI installed and configured (`aws configure`)  
- AWS CDK installed (`npm install -g aws-cdk`)  
- Python installed (`python --version`)  
- An IDE such as VS Code  

---

## **Step 1: Set Up the AWS CDK Project**  
1. **Create a new directory and initialize a CDK project:**  
   ```sh
   mkdir nested-stack-lab
   cd nested-stack-lab
   cdk init app --language python
   ```
2. **Create and activate a virtual environment:**  
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv/Scripts/activate
   ```
3. **Install dependencies:**  
   ```sh
   pip install -r requirements.txt
   ```

---

## **Step 2: Create the Nested VPC Stack**
1. Inside the `nested_stack_lab` folder, create a new file named `network_stack.py`.  
2. Add the following code to create a VPC in a **nested stack**:  

```python
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

class NetworkStack(cdk.NestedStack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        self.vpc = ec2.Vpc(
            self, "MyNestedVPC",
            max_azs=2
        )

        # Output VPC ID
        cdk.CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
```

---

## **Step 3: Create the Nested EC2 Stack**
1. Inside the `nested_stack_lab` folder, create a new file named `compute_stack.py`.  
2. Add the following code to launch an EC2 instance inside the **nested VPC stack**:  

```python
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct
class ComputeStack(cdk.NestedStack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create a Security Group for EC2
        security_group = ec2.SecurityGroup(
            self, "MySecurityGroup",
            vpc=vpc,
            description="Allow SSH access",
            allow_all_outbound=True
        )
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH access")

        # Create an EC2 instance
        ec2.Instance(
            self, "MyEC2Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinuxImage(),
            vpc=vpc,
            security_group=security_group
        )
```

---

## **Step 4: Create the Root Stack (MainStack)**
1. Open `lib/nested_stack_lab_stack.py` and replace the contents with the following code:  

```python
import aws_cdk as cdk
from constructs import Construct
from nested_stack_lab.compute_stack import ComputeStack
from nested_stack_lab.network_stack import NetworkStack

class MainStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create the Nested VPC Stack
        network_stack = NetworkStack(self, "NetworkNestedStack")

        # Create the Nested Compute Stack and pass the VPC reference
        ComputeStack(self, "ComputeNestedStack", vpc=network_stack.vpc)
```

---

## **Step 5: Modify `app.py` to Deploy the Stacks**
1. Open `app.py` and modify it as follows:

```python
#!/usr/bin/env python3
import aws_cdk as cdk
from nested_stack_lab_stack import MainStack

app = cdk.App()
MainStack(app, "NestedStackLab")
app.synth()
```

---

## **Step 6: Deploy the Nested Stacks**
1. Bootstrap the CDK environment (if not already done):
   ```sh
   cdk bootstrap
   ```
2. Synthesize the CloudFormation templates:
   ```sh
   cdk synth
   ```
3. Deploy the entire nested stack:
   ```sh
   cdk deploy
   ```

---

## **Step 7: Verify Deployment**
- Go to the **AWS CloudFormation Console** and check that `NestedStackLab` is deployed.  
- Inside `NestedStackLab`, you will find `NetworkNestedStack` and `ComputeNestedStack` as child stacks.  
- Go to the **AWS VPC Console** to verify that the VPC was created.  
- Go to the **AWS EC2 Console** to confirm that an EC2 instance is running inside the VPC.  

---

## **Step 8: Cleanup**
To delete all created resources:
```sh
cdk destroy
```

---

## **Conclusion**
✅ Created a **MainStack** that contains **nested stacks**  
✅ Created a **NetworkStack** that provisions a VPC  
✅ Created a **ComputeStack** that provisions an EC2 instance inside the VPC  
✅ Used **Nested Stacks** to modularize and manage infrastructure  

This lab demonstrates how **AWS CDK Nested Stacks** help in managing large and complex infrastructures efficiently. Let me know if you need any modifications! 🚀
