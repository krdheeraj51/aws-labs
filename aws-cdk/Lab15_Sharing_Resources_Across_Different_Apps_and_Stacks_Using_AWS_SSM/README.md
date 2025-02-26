# **Lab 15: Sharing Resources Across Different Apps and Stacks Using AWS SSM Parameter Store**

## **Objective**
In this lab, we will:  
✅ Use **AWS SSM Parameter Store** to share resources between multiple AWS CDK stacks.  
✅ Store resource ARNs in **SSM Parameters** and retrieve them in another stack.  
✅ Demonstrate **cross-stack resource sharing** using **AWS CDK (Python)**.

---

## **Prerequisites**
- **AWS CLI** configured (`aws configure`)  
- **AWS CDK installed** (`npm install -g aws-cdk`)  
- **Python 3.x** installed (`python3 --version`)  
- **AWS IAM permissions** to manage SSM parameters, Lambda, S3, and IAM  

---

## **Step 1: Initialize a New AWS CDK Project**
```sh
mkdir cross-stack-ssm && cd cross-stack-ssm
cdk init app --language=python
```
Activate the virtual environment:

**For Mac/Linux:**  
```sh
source .venv/bin/activate
```
**For Windows:**  
```sh
.venv/Scripts/activate
```

Install dependencies:
```sh
pip install aws-cdk-lib constructs
```

---

## **Step 2: Create a Resource Stack (Producer Stack)**  
This stack **creates resources** (S3 bucket and IAM role) and **stores their ARNs in SSM Parameters**.

Modify **`cross_stack_ssm/cross_stack_ssm_stack.py`**:

```python
from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_iam as iam,
    aws_ssm as ssm
)

class ResourceProducerStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "SharedBucket",
                           versioned=True,
                           removal_policy=cdk.RemovalPolicy.DESTROY)

        # Create an IAM Role
        role = iam.Role(self, "SharedRole",
                        assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))

        # Store resource ARNs in SSM Parameter Store
        ssm.StringParameter(self, "BucketArnParameter",
                            parameter_name="/shared-resources/s3-bucket-arn",
                            string_value=bucket.bucket_arn)

        ssm.StringParameter(self, "RoleArnParameter",
                            parameter_name="/shared-resources/iam-role-arn",
                            string_value=role.role_arn)
```

---

## **Step 3: Create a Consumer Stack (User Stack)**  
This stack **retrieves the ARNs from SSM Parameters** and uses them.

Create a new file **`consumer_stack.py`** inside the `cross_stack_ssm/` folder:

📄 **`cross_stack_ssm/consumer_stack.py`**
```python
from aws_cdk import (
    core as cdk,
    aws_ssm as ssm,
    aws_lambda as _lambda
)

class ResourceConsumerStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Retrieve the S3 bucket ARN from SSM
        bucket_arn = ssm.StringParameter.value_for_string_parameter(
            self, "/shared-resources/s3-bucket-arn")

        # Retrieve the IAM Role ARN from SSM
        role_arn = ssm.StringParameter.value_for_string_parameter(
            self, "/shared-resources/iam-role-arn")

        # Create a Lambda function using the shared role and bucket ARN
        self.lambda_function = _lambda.Function(
            self, "SSMConsumerLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "BUCKET_ARN": bucket_arn,
                "ROLE_ARN": role_arn
            }
        )
```

---

## **Step 4: Create a Lambda Function to Use Shared Resources**
Create a **`lambda/`** directory and add **`lambda_function.py`** inside it:

📄 **`lambda/lambda_function.py`**
```python
import os

def lambda_handler(event, context):
    bucket_arn = os.environ.get('BUCKET_ARN')
    role_arn = os.environ.get('ROLE_ARN')

    return {
        "Shared S3 Bucket ARN": bucket_arn,
        "Shared IAM Role ARN": role_arn
    }
```

---

## **Step 5: Modify `app.py` to Include Both Stacks**
Modify **`app.py`** to add both stacks:

📄 **`app.py`**
```python
#!/usr/bin/env python3
import aws_cdk as cdk
from cross_stack_ssm.cross_stack_ssm_stack import ResourceProducerStack
from cross_stack_ssm.consumer_stack import ResourceConsumerStack

app = cdk.App()

producer_stack = ResourceProducerStack(app, "ResourceProducerStack")
consumer_stack = ResourceConsumerStack(app, "ResourceConsumerStack")

# Make sure Consumer Stack deploys AFTER Producer Stack
consumer_stack.add_dependency(producer_stack)

app.synth()
```

---

## **Step 6: Deploy the Stacks**
Run the following commands:
```sh
cdk synth
cdk deploy
```

### **Expected Output:**
- **ResourceProducerStack** creates **S3 Bucket & IAM Role** and stores their ARNs in SSM.
- **ResourceConsumerStack** retrieves the ARNs and **uses them in Lambda**.

---

## **Step 7: Invoke the Lambda to Verify**
```sh
aws lambda invoke --function-name SSMConsumerLambda response.json
cat response.json
```
**Expected Output:**
```json
{
    "Shared S3 Bucket ARN": "arn:aws:s3:::cdk-shared-bucket-123456",
    "Shared IAM Role ARN": "arn:aws:iam::123456789012:role/cdk-shared-role"
}
```

---

## **Step 8: Cleanup (Optional)**
To delete all resources:
```sh
cdk destroy
```

---

## **Summary**
✅ **Stored resource ARNs in SSM Parameter Store**  
✅ **Retrieved shared resources across different stacks**  
✅ **Used AWS CDK to deploy multiple stacks efficiently**  

This approach makes it **easy to share resources** across applications and **improves maintainability**! 🚀