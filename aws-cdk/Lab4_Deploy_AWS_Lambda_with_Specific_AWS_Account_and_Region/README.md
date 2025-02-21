# Lab 4: Deploy AWS Lambda with a Specific AWS Account and Region using AWS CDK in Python
## Objective
The objective of this lab is to create and deploy an AWS Lambda function using AWS CDK in Python while explicitly specifying an **AWS Account and Region**. This will help you understand how to manage deployments across different AWS environments.

## Prerequisites
- AWS account
- AWS CLI installed and configured
- Node.js installed
- AWS CDK installed (`npm install -g aws-cdk`)
- Python installed (recommended: Python 3.8 or later)
- An IDE such as VSCode

## Steps

### **Step 1: Set Up Your AWS CDK Project**  
1. **Create a new project directory** and open it in your terminal:
```
  mkdir lambda-cdk-lab
  cd lambda-cdk-lab
```
3. **Initialize the AWS CDK project** with Python:  
```
   cdk init app --language python
```
4. **Create a virtual environment and activate it**:  
```
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
5. **Install dependencies**:  
```
   pip install -r requirements.txt
```

---

### **Step 2: Define Lambda Function**  
1. Inside the *lambda-cdk-lab* directory, create a lambda folder to store the Lambda function code:
```
mkdir lambda
```
2. Create a new Python file inside lambda/ named lambda_function.py and add the following content::  
   ```python
   def handler(event, context):
    print("Hello from AWS Lambda!")
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
   ```

---

### **Step 3: Modify the CDK Stack**  
1. Open lambda_cdk_lab/lambda_cdk_lab_stack.py and modify it as follows:
If this is your first time using AWS CDK, run:  
```python
from aws_cdk import (
    Stack,
    aws_lambda as _lambda
)
from constructs import Construct
class LambdaCdkLabStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        lambdaFn = _lambda.Function(
            self, "LambdaCdkLabFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("lambda")
        )

```
2. Open app.py and modify it to include AWS account and region:
```python
import aws_cdk as cdk

from lambda_cdk_lab.lambda_cdk_lab_stack import LambdaCdkLabStack
app = cdk.App()
env = cdk.Environment(account="YOUR_AWS_ACCOUNT_ID", region="YOUR_AWS_REGION")
LambdaCdkLabStack(app, "LambdaCdkLabStack",env=env
   
)

app.synth()

```
##### Replace:
- "YOUR_AWS_ACCOUNT_ID" with your actual AWS account ID (e.g., 123456789012)
- "YOUR_AWS_REGION" with the desired region (e.g., us-east-1)
---
### **Step 4: Bootstrap** 
1. Bootstrap the AWS environment (only required once per AWS account/region):
```
cdk bootstrap
```

### **Step 4: Synthesize the CloudFormation Template**  
Run the following command to generate the AWS CloudFormation template:  
```
cdk synth
```
This will output a CloudFormation template based on the defined CDK stack.

---

### **Step 5: Deploy the Stack**  
1. Deploy the stack using:  
   ```
   cdk deploy
   ```
2. Confirm the deployment when prompted.

---

### **Step 6: Monitor the Deployment**  
- Navigate to the **AWS CloudFormation console** to view the stack creation progress.  
- Wait for the status to change from **"CREATE_IN_PROGRESS"** to **"CREATE_COMPLETE"**.  
- Verify the lambda in the **AWS lambda console** after selecting specified region.  
- Test the function using the AWS console or AWS CLI
---

### **Step 7: Clean Up Resources**  
To delete the lambda and all related resources, run:  
```
cdk destroy
```
This ensures that no unnecessary AWS resources remain in your account.

---

## Conclusion
- In this lab, you have successfully:

✅ Created an AWS Lambda function using AWS CDK in Python

✅ Deployed it with a specific AWS Account and Region

✅ Learned how to manage AWS deployments using Infrastructure as Code (IaC)
