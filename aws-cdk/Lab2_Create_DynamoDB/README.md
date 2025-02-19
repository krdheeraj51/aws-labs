# Lab 2: Create AWS DynamoDB using AWS CDK

## Objective
The objective of this lab is to create an Amazon DynamoDB table using AWS CDK in Python. By completing this lab, participants will understand how to define and deploy a DynamoDB table programmatically using Infrastructure as Code (Ia

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
  mkdir dynamodb-cdk-lab
  cd dynamodb-cdk-lab
```
2. **Initialize the AWS CDK project** with Python:  
```
   cdk init app --language python
```
3. **Create a virtual environment and activate it**:  
```
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
4. **Install dependencies**:  
```
   pip install -r requirements.txt
```

---

### **Step 2: Define DynamoDB Table**  
1. Open dynamodb_cdk_lab/dynamodb_cdk_lab_stack.py and modify it as follows: 
```python
from aws_cdk import core
import aws_cdk.aws_dynamodb as dynamodb

class DynamoDbCdkLabStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        table = dynamodb.Table(
            self, "MyDynamoDBTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            table_name="MyDynamoDBTable",
            removal_policy=core.RemovalPolicy.DESTROY  # Use cautiously in production
        )   
```
---
### **Step 3: Bootstrap** 
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
- Verify the  DynamoDB table in the **AWS DynamoDB Console**.  

---

### **Step 7: Clean Up Resources**  
To delete the  DynamoDB table  and all related resources, run:  
```
cdk destroy
```
This ensures that no unnecessary AWS resources remain in your account.

---
