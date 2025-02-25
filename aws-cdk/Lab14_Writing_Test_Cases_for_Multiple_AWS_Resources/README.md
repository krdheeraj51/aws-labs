## **Lab 14: Writing Test Cases for Multiple AWS Resources in AWS CDK**  

### **Objective**  
This lab will demonstrate:  

✅ Defining **multiple AWS resources** in AWS CDK (S3 Bucket, DynamoDB Table, and Lambda Function).  

✅ Writing **test cases** to validate these resources using **AWS CDK assertions**.  

✅ Running tests before deployment to ensure correctness.  

---

### **Prerequisites**  
- AWS CDK installed (`npm install -g aws-cdk`)  
- Python installed (`python3 --version`)  
- AWS CLI configured (`aws configure`)  
- Basic knowledge of AWS CDK, Python, and testing with `pytest`  

---

### **Step 1: Initialize a New AWS CDK Project**  
Run the following commands to set up a new AWS CDK project in Python:  

```sh
mkdir cdk-multi-resource-testing && cd cdk-multi-resource-testing
cdk init app --language=python
```

Activate the virtual environment:  

**For Mac/Linux:**  
```sh
source .venv/bin/activate
```

**For Windows:**  
```sh
.venv\Scripts\activate
```

Install dependencies:  
```sh
pip install -r requirements.txt
```

---

### **Step 2: Define Multiple AWS Resources in the CDK Stack**  
Modify the **`cdk_multi_resource_testing/cdk_multi_resource_testing_stack.py`** file:  

```python
from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as _lambda

class CdkMultiResourceTestingStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # S3 Bucket
        self.s3_bucket = s3.Bucket(self, "MyTestBucket",
                                   versioned=True,
                                   removal_policy=cdk.RemovalPolicy.DESTROY)

        # DynamoDB Table
        self.dynamo_table = dynamodb.Table(
            self, "MyTestTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Lambda Function
        self.lambda_function = _lambda.Function(
            self, "MyTestLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda")
        )
```

## **Step 3: Add Lambda Function Code**
1. Create a `lambda/` directory inside the project:
   ```sh
   mkdir lambda
   ```
2. Inside `lambda/`, create a file called `index.py`:
   ```python
   def lambda_handler(event, context):
       return {"statusCode": 200, "body": "Deployment Successful!"}
   ```
3. Add `requirements.txt` for dependencies:
   ```sh
   touch requirements.txt
   ```
---

### **Step 4: Install Testing Dependencies**  
We need `pytest` for testing and `aws-cdk-lib` for assertions.  

Run the following command:  
```sh
pip install pytest aws-cdk-lib constructs
```

---

### **Step 5: Write Test Cases for the Resources**  
Create a **`tests/`** directory and add a test file inside it:  

📄 **`tests/test_cdk_multi_resource_testing.py`**  

```python
import aws_cdk as core
import aws_cdk.assertions as assertions
from cdk_multi_resource_testing.cdk_multi_resource_testing_stack import CdkMultiResourceTestingStack

def test_s3_bucket_created():
    app = core.App()
    stack = CdkMultiResourceTestingStack(app, "MyTestStack")

    template = assertions.Template.from_stack(stack)

    # Assert that an S3 Bucket is created
    template.resource_count_is("AWS::S3::Bucket", 1)

def test_dynamodb_table_created():
    app = core.App()
    stack = CdkMultiResourceTestingStack(app, "MyTestStack")

    template = assertions.Template.from_stack(stack)

    # Assert that a DynamoDB Table is created
    template.resource_count_is("AWS::DynamoDB::Table", 1)

def test_lambda_function_created():
    app = core.App()
    stack = CdkMultiResourceTestingStack(app, "MyTestStack")

    template = assertions.Template.from_stack(stack)

    # Assert that a Lambda function is created
    template.resource_count_is("AWS::Lambda::Function", 1)
```

---

### **Step 6: Run the Tests**  
Execute the tests using:  
```sh
pytest
```
If successful, the output should be similar to:  
```
========================= test session starts =========================
collected 3 items

tests/test_cdk_multi_resource_testing.py ...                     [100%]

========================== 3 passed in 0.42s ==========================
```

---

### **Step 6: Debugging & Improvements**  
- If any test fails, check the error message and update the CDK stack accordingly.  
- Add additional assertions to check **resource properties** (e.g., DynamoDB key schema, Lambda runtime).  
- Use `pytest -v` for detailed test output.  

---

### **Step 7 (Optional): Deploy the Stack**  
Once tests pass, you can deploy the stack to AWS:  
```sh
cdk synth
cdk deploy
```

---

### **Summary**  
✅ **Created AWS resources** (S3, DynamoDB, Lambda) using AWS CDK.  

✅ **Wrote test cases** to validate these resources before deployment.  

✅ **Ran tests successfully** to ensure infrastructure correctness.  

This approach helps **prevent misconfigurations** and **improves AWS infrastructure quality** 🚀