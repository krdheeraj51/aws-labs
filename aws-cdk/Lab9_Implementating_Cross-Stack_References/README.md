# **Lab 9: Implementating Cross-Stack References in AWS CDK**

## **Objective**
The objective of this lab is to demonstrate how to use **cross-stack references** in AWS CDK. We will create:  
1. **A VPC in one stack (NetworkStack)**  
2. **An EC2 instance in another stack (ComputeStack) that references the VPC from NetworkStack**  

By completing this lab, you will learn how to share resources across stacks efficiently using AWS CDK.

---

## **Prerequisites**
- AWS account with IAM access  
- AWS CLI installed and configured (`aws configure`)  
- Node.js installed (`node -v`)  
- AWS CDK installed (`npm install -g aws-cdk`)  
- Python installed (`python --version`)  
- An IDE such as VS Code  

---

## **Steps to Implement Cross-Stack References in AWS CDK**

### **Step 1: Setup AWS CDK Project**
1. **Create a new directory and initialize the CDK project:**
   ```sh
   mkdir cross-stack-lab
   cd cross-stack-lab
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

### **Step 2: Create Network Stack (VPC)**
1. Navigate to the `cross_stack_lab` folder and open `cross_stack_lab_stack.py`.  
2. Create a new file named `network_stack.py` and add the following code:  

```python
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

class NetworkStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        self.vpc = ec2.Vpc(
            self, "MyVPC",
            max_azs=2
        )

        # Export VPC ID to be used in another stack
        cdk.CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
```

---

### **Step 3: Create Compute Stack (EC2 Instance)**
1. Create a new file named `compute_stack.py` and add the following code:

```python
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct
from network_stack import NetworkStack

class ComputeStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, network_stack: NetworkStack, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Use the VPC from NetworkStack
        vpc = network_stack.vpc

        # Create an EC2 Security Group
        security_group = ec2.SecurityGroup(
            self, "MySecurityGroup",
            vpc=vpc,
            description="Allow SSH access",
            allow_all_outbound=True
        )
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH access")

        # Launch an EC2 instance in the shared VPC
        ec2.Instance(
            self, "MyEC2Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinuxImage(),
            vpc=vpc,
            security_group=security_group
        )
```

---

### **Step 4: Modify `app.py` to Include Both Stacks**
Modify `app.py` to deploy both stacks in order:

```python
#!/usr/bin/env python3
import aws_cdk as cdk
import sys
sys.path.insert(0, './cross_stack_lab')
from network_stack import NetworkStack
from compute_stack import ComputeStack

app = cdk.App()

# Create Network Stack
network_stack = NetworkStack(app, "NetworkStack")

# Create Compute Stack and pass the VPC reference
compute_stack = ComputeStack(app, "ComputeStack", network_stack=network_stack)

app.synth()
```

---

### **Step 5: Deploy the Stacks**
1. Bootstrap the CDK environment (if not already done):
   ```sh
   cdk bootstrap
   ```
2. Synthesize the CloudFormation templates:
   ```sh
   cdk synth
   ```
3. Deploy both stacks:
   ```sh
   cdk deploy
   ```

---

### **Step 6: Verify Deployment**
- Go to the **AWS CloudFormation Console** and verify that both `NetworkStack` and `ComputeStack` are successfully deployed.  
- Open the **AWS VPC Console** and check that the VPC has been created.  
- Open the **AWS EC2 Console** and confirm that the instance is running inside the created VPC.  

---

### **Step 7: Cleanup**
To delete all created resources:
```sh
cdk destroy
```

---

## **Conclusion**
✅ Created a **Network Stack** with a VPC  

✅ Created a **Compute Stack** with an EC2 instance that references the VPC  

✅ Used **Cross-Stack References** to share the VPC between stacks  

✅ Deployed everything using **AWS CDK**  

You now have a **modular AWS CDK project** that uses cross-stack references! 🚀  

---

This lab demonstrates how AWS CDK allows you to **separate concerns into multiple stacks** while keeping resources modular and reusable. Let me know if you need further explanations! 😊
