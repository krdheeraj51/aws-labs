# Lab 5: Create a CloudWatch Alarm for AWS Lambda using AWS CDK in Python
## Objective
The goal of this lab is to create an AWS Lambda function and set up a CloudWatch Alarm to monitor its invocation errors. This will help you understand how to configure AWS monitoring using Infrastructure as Code (IaC) with AWS CDK.

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
  mkdir lambda-cloudwatch-lab
  cd lambda-cloudwatch-lab
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
import json

def handler(event, context):
    print("Lambda function executed!")
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from Lambda!")
    }
```
---

### **Step 3: Modify the CDK Stack**  
1. Open lambda_cloudwatch_lab/lambda_cloudwatch_lab_stack.py and modify it as follows:
```python
from aws_cdk import core
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_cloudwatch as cloudwatch

class LambdaCloudWatchLabStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the Lambda function
        lambda_function = _lambda.Function(
            self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("lambda")
        )

        # Create a CloudWatch Alarm for Lambda errors
        lambda_error_alarm = cloudwatch.Alarm(
            self, "LambdaErrorAlarm",
            metric=lambda_function.metric_errors(),
            threshold=1,  # Trigger alarm if 1 or more errors occur
            evaluation_periods=1,
            alarm_description="Alarm when Lambda function has 1 or more errors",
            alarm_name="LambdaErrorAlarm"
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
- Go to the AWS CloudWatch Console → Alarms.
- Find the alarm named LambdaErrorAlarm
- You can test the alarm by forcing Lambda errors, such as raising an exception in lambda_function.py:
```python
def handler(event, context):
    raise Exception("Simulated Lambda Error")
```
- Then invoke the Lambda function and check CloudWatch Alarms.
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

✅ Created an AWS Lambda function using AWS CDK

✅ Configured a CloudWatch Alarm to monitor Lambda errors

✅ Learned how to set up monitoring in AWS using IaC
