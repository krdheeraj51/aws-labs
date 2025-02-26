# **Lab 16: Sharing Resources Across Different Apps and Stacks Using `CfnOutput` in AWS CDK**  

## **Objective**  
In this lab, we will:  
✅ Use **AWS CDK's `CfnOutput`** to share resource values between multiple stacks.  
✅ Store an **S3 bucket name** and **IAM role ARN** in `CfnOutput`.  
✅ Retrieve and use the outputs in another stack using **AWS CDK (Python)**.  

---

## **Prerequisites**  
- **AWS CLI** configured (`aws configure`)  
- **AWS CDK installed** (`npm install -g aws-cdk`)  
- **Python 3.x** installed (`python3 --version`)  
- **AWS IAM permissions** to manage S3, IAM, and Lambda  

---

## **Step 1: Initialize a New AWS CDK Project**  
```sh
mkdir cross-stack-cfnoutput && cd cross-stack-cfnoutput
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

## **Step 2: Create a Producer Stack**  
This stack **creates an S3 bucket and IAM role** and **exports their names using `CfnOutput`**.

Modify **`cross_stack_cfnoutput/cross_stack_cfnoutput_stack.py`**:

📄 **`producer_stack.py`**
```python
from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_iam as iam
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

        # Export the Bucket Name and Role ARN using CfnOutput
        cdk.CfnOutput(self, "BucketNameOutput",
                      value=bucket.bucket_name,
                      export_name="SharedBucketName")

        cdk.CfnOutput(self, "RoleArnOutput",
                      value=role.role_arn,
                      export_name="SharedRoleArn")
```

---

## **Step 3: Create a Consumer Stack**  
This stack **retrieves the exported values** from `CfnOutput` and uses them.

Create a new file **`consumer_stack.py`** inside the `cross_stack_cfnoutput/` folder:

📄 **`consumer_stack.py`**
```python
from aws_cdk import (
    core as cdk,
    aws_lambda as _lambda,
    aws_ssm as ssm
)

class ResourceConsumerStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Import values from CfnOutput
        bucket_name = cdk.Fn.import_value("SharedBucketName")
        role_arn = cdk.Fn.import_value("SharedRoleArn")

        # Create a Lambda function using the shared role and bucket name
        self.lambda_function = _lambda.Function(
            self, "CfnOutputConsumerLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "BUCKET_NAME": bucket_name,
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
    bucket_name = os.environ.get('BUCKET_NAME')
    role_arn = os.environ.get('ROLE_ARN')

    return {
        "Shared S3 Bucket Name": bucket_name,
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
from cross_stack_cfnoutput.producer_stack import ResourceProducerStack
from cross_stack_cfnoutput.consumer_stack import ResourceConsumerStack

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
- **ResourceProducerStack** creates an **S3 Bucket & IAM Role** and exports values.  
- **ResourceConsumerStack** retrieves the exported values and **uses them in Lambda**.  

---

## **Step 7: Invoke the Lambda to Verify**  
```sh
aws lambda invoke --function-name CfnOutputConsumerLambda response.json
cat response.json
```
### **Expected Output:**  
```json
{
    "Shared S3 Bucket Name": "cdk-shared-bucket-123456",
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
✅ **Stored resource values using `CfnOutput`**  
✅ **Retrieved shared resources across stacks**  
✅ **Used AWS CDK to efficiently deploy multiple stacks**  

This approach makes **sharing resources easy and scalable** across AWS stacks! 🚀