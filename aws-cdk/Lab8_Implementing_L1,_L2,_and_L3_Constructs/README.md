# Lab 8: Implementing L1, L2, and L3 Constructs in AWS CDK

## Objective
The objective of this lab is to demonstrate the differences between L1, L2, and L3 constructs in AWS CDK by implementing an S3 bucket using each construct type. By completing this lab, participants will:

- Understand the concept of AWS CDK Constructs (L1, L2, L3)
- Learn how to define resources at different abstraction levels
- Deploy and verify an S3 bucket using AWS CDK
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
mkdir l1-l2-l3-cdk-lab
cd l1-l2-l3-cdk-lab
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
1. Open `l1_l2_l3_cdk_lab/l1_l2_l3_cdk_lab_stack.py` and modify it as follows:
```python
import aws_cdk as cdk
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_s3_deployment as s3_deployment
import aws_cdk.aws_s3 as s3_l1
from constructs import Construct
class L1L2L3CdkLabStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # L1 Construct (Low-Level: CloudFormation representation)
        l1_bucket = s3_l1.CfnBucket(
            self, "L1Bucket",
            bucket_name="my-l1-bucket",
            versioning_configuration={"status": "Enabled"}
        )

        # L2 Construct (High-Level: CDK abstraction)
        l2_bucket = s3.Bucket(
            self, "L2Bucket",
            bucket_name="my-l2-bucket",
            versioned=True
        )

        # L3 Construct (Pattern: Deploys files into S3)
        l3_bucket_deployment = s3_deployment.BucketDeployment(
            self, "L3BucketDeployment",
            sources=[s3_deployment.Source.asset("./sample-files")],  # Folder containing files to upload
            destination_bucket=l2_bucket
        )
 
```
### Step 4: Add Sample Files for Deployment
1. Inside your project directory, create a folder called `sample-files`:
```sh
mkdir sample-files
```
2. Add a sample text file inside it:
```sh
echo "Hello, this is an L3 construct demo!" > sample-files/index.txt
```

### Step 5: Deploy the Stack
1. **Bootstrap CDK (if not done earlier):**
```sh
cdk bootstrap
```
2. **Synthesize and Deploy:**
```sh
cdk synth
cdk deploy
```

### Step 6: Verify Deployment
1. Go to **AWS S3 Console**.
2. You should see:
   - `my-l1-bucket` (created via L1)
   - `my-l2-bucket` (created via L2)
   - Inside `my-l2-bucket`, you should find the `index.txt` file, which was deployed using the L3 construct.

### Step 7: Cleanup
To remove all resources:
```sh
cdk destroy
```

## Conclusion
✅ Created an **S3 bucket** using **L1 Construct (CfnBucket)**

✅ Defined an **S3 bucket** using **L2 Construct (Bucket)**

✅ Deployed files into the bucket using **L3 Construct (BucketDeployment)**

✅ Deployed everything using **AWS CDK**

This lab effectively demonstrates **all three levels of AWS CDK Constructs** in a **single project**! 🚀
