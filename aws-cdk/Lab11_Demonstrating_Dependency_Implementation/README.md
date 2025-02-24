# **Lab 11: Demonstrating Dependency Implementation in AWS CDK**  

## **Objective**  
The goal of this lab is to **demonstrate dependency handling in AWS CDK**. When defining multiple resources, sometimes one resource depends on another (e.g., an EC2 instance depends on a VPC). In AWS CDK, we can **explicitly define dependencies** to ensure proper resource creation order.  

### **What We Will Implement**
We will create:  
1. **A VPC Stack (`NetworkStack`)** → Creates a VPC  
2. **An S3 Stack (`StorageStack`)** → Creates an S3 bucket  
3. **A Compute Stack (`ComputeStack`)** → Launches an EC2 instance **after** the VPC and S3 bucket are created  

We'll use **AWS CDK's `add_dependency` method** to ensure that:  
✅ The **EC2 instance** is launched **only after** the VPC is available  
✅ The **EC2 instance** is created **only after** the S3 bucket is available  

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
   mkdir dependency-lab
   cd dependency-lab
   cdk init app --language python
   ```
2. **Create and activate a virtual environment:**  
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies:**  
   ```sh
   pip install -r requirements.txt
   ```

---

## **Step 2: Create the Network Stack**
1. Inside the `lib` folder, create a new file named `network_stack.py`.  
2. Add the following code to create a VPC:  

```python
from aws_cdk import cdk
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

        # Output VPC ID
        cdk.CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
```

---

## **Step 3: Create the Storage Stack**
1. Inside the `lib` folder, create a new file named `storage_stack.py`.  
2. Add the following code to create an S3 bucket:  

```python
import aws_cdk  as cdk
from constructs import Construct
import aws_cdk.aws_s3 as s3

class StorageStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        self.bucket = s3.Bucket(
            self, "MyBucket",
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Output S3 Bucket Name
        cdk.CfnOutput(self, "BucketName", value=self.bucket.bucket_name)
```

---

## **Step 4: Create the Compute Stack (EC2)**
1. Inside the `lib` folder, create a new file named `compute_stack.py`.  
2. Add the following code to launch an EC2 instance **after** the VPC and S3 bucket are created:  

```python
import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_s3 as s3

class ComputeStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, bucket: s3.Bucket, **kwargs):
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
        ec2_instance = ec2.Instance(
            self, "MyEC2Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinuxImage(),
            vpc=vpc,
            security_group=security_group
        )

        # Explicit Dependency on S3 Bucket
        ec2_instance.node.add_dependency(bucket)
```

---

## **Step 5: Create the Main Stack**
1. Open `lib/dependency_lab_stack.py` and replace the contents with the following code:  

```python
import aws_cdk as cdk
from constructs import Construct
from network_stack import NetworkStack
from storage_stack import StorageStack
from compute_stack import ComputeStack

class MainStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create the VPC Stack
        network_stack = NetworkStack(self, "NetworkStack")

        # Create the Storage Stack
        storage_stack = StorageStack(self, "StorageStack")

        # Create the Compute Stack and pass the dependencies
        compute_stack = ComputeStack(self, "ComputeStack", vpc=network_stack.vpc, bucket=storage_stack.bucket)

        # Explicitly add dependencies
        compute_stack.add_dependency(network_stack)
        compute_stack.add_dependency(storage_stack)
```

---

## **Step 6: Modify `app.py` to Deploy the Stacks**
1. Open `app.py` and modify it as follows:

```python
#!/usr/bin/env python3
import aws_cdk as cdk
from dependency_lab_stack import MainStack

app = cdk.App()
MainStack(app, "DependencyLab")
app.synth()
```

---

## **Step 7: Deploy the Stacks**
1. Bootstrap the CDK environment (if not already done):
   ```sh
   cdk bootstrap
   ```
2. Synthesize the CloudFormation templates:
   ```sh
   cdk synth
   ```
3. Deploy the entire stack:
   ```sh
   cdk deploy
   ```

---

## **Step 8: Verify the Deployment**
- Go to the **AWS CloudFormation Console** and check that:  
  ✅ `NetworkStack` is deployed first  
  ✅ `StorageStack` is deployed second  
  ✅ `ComputeStack` is deployed last (depends on both `NetworkStack` and `StorageStack`)  
- Go to the **AWS EC2 Console** to verify that an EC2 instance is running inside the VPC.  
- Go to the **AWS S3 Console** to confirm that an S3 bucket has been created.  

---

## **Step 9: Cleanup**
To delete all created resources:
```sh
cdk destroy
```

---

## **Conclusion**
✅ Used **`add_dependency()`** to explicitly control resource creation order  
✅ Created **three separate stacks** (VPC, S3, EC2) and managed dependencies between them  
✅ Ensured that the EC2 instance was created **only after** the S3 bucket and VPC were available  

This lab demonstrates **AWS CDK dependencies** and how to ensure proper resource provisioning order. Let me know if you need any modifications! 🚀