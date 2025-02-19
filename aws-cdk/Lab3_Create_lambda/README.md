# Lab 3: Create AWS Lambda using AWS CDK

## Objective
The objective of this lab is to create an AWS Lambda function using AWS CDK in Python. By completing this lab, participants will understand how to define and deploy AWS Lambda functions programmatically using Infrastructure as Code (IaC).

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
1. Inside the lambda-cdk-lab directory, create a lambda folder to store the Lambda function code:
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
from aws_cdk import core
import aws_cdk.aws_lambda as _lambda

class LambdaCdkLabStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_function = _lambda.Function(
            self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("lambda")
        )
```
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
- Verify the lambda in the **AWS lambda console**.  

---

### **Step 7: Clean Up Resources**  
To delete the lambda and all related resources, run:  
```
cdk destroy
```
This ensures that no unnecessary AWS resources remain in your account.

---
