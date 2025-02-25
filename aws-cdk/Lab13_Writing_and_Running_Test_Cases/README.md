## **Lab 13: Writing and Running Test Cases for AWS CDK in Python**  

### **Objective**  
In this lab, we will:  
- Create an **AWS CDK project** in Python.  
- Define a simple **AWS resource (S3 Bucket)**.  
- Write and run **test cases** using **pytest** and **AWS CDK assertions**.  
- Ensure infrastructure validation **before deployment**.  

---

### **Prerequisites**  
- AWS CDK installed (`npm install -g aws-cdk`)  
- Python installed (`python3 --version`)  
- AWS CLI configured (`aws configure`)  
- Basic knowledge of AWS CDK and Python  

---

### **Step 1: Initialize a New AWS CDK Project**  
Run the following commands to set up a new AWS CDK project in Python:  
```sh
mkdir cdk-testing-lab && cd cdk-testing-lab
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

### **Step 2: Implement a Simple AWS CDK Stack**  
We will create an **S3 Bucket** in AWS CDK.  

Modify the **`cdk_testing_lab/cdk_testing_lab_stack.py`** file:  

```python
import aws_cdk as cdk
from aws_cdk import aws_s3 as s3

class CdkTestingLabStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        s3.Bucket(self, "MyTestBucket",
                  versioned=True,
                  removal_policy=cdk.RemovalPolicy.DESTROY)
```

---

### **Step 3: Install Testing Dependencies**  
We need **pytest** for running tests and **AWS CDK assertions** for validating CDK constructs.  

Run the following command:  
```sh
pip install pytest aws-cdk-lib constructs
```

---

### **Step 4: Write Test Cases**  
Create a new directory **`tests/`** and inside it, create a test file:  

📄 **`tests/test_cdk_testing_lab.py`**  
```python
import aws_cdk as core
import aws_cdk.assertions as assertions
from cdk_testing_lab.cdk_testing_lab_stack import CdkTestingLabStack

def test_s3_bucket_created():
    app = core.App()
    stack = CdkTestingLabStack(app, "MyTestStack")

    # Generate CloudFormation template
    template = assertions.Template.from_stack(stack)

    # Assert that an S3 Bucket is created
    template.resource_count_is("AWS::S3::Bucket", 1)
```

---

### **Step 5: Run the Tests**  
Run the test cases using:  
```sh
pytest
```
If successful, you will see output like:  
```
========================= test session starts =========================
collected 1 item

tests/test_cdk_testing_lab.py .                                  [100%]

========================== 1 passed in 0.34s ==========================
```

---

### **Step 6: Synthesize and Deploy (Optional)**  
You can verify the AWS CDK stack:  
```sh
cdk synth
cdk deploy
```

---

### **Summary**  
✅ **Created an AWS CDK Stack** with an S3 Bucket. 

✅ **Installed testing dependencies (pytest & assertions)**.  

✅ **Wrote test cases to validate the infrastructure**.  

✅ **Ran tests successfully** before deployment.  

---

## **Lab 2: Step-by-Step Guide to Writing Test Cases in AWS CDK (Python)**  
This lab provides **only steps** to write test cases without any setup for CI/CD.

### **Step 1: Install Testing Dependencies**  
Run:  
```sh
pip install pytest aws-cdk-lib constructs
```

---

### **Step 2: Create a Test Directory**  
Navigate to your AWS CDK project and create a folder:  
```sh
mkdir tests
```

---

### **Step 3: Write Test Cases**  
Create a test file **`tests/test_cdk_testing_lab.py`** with the following content:  

```python
import aws_cdk as core
import aws_cdk.assertions as assertions
from cdk_testing_lab.cdk_testing_lab_stack import CdkTestingLabStack

def test_s3_bucket_created():
    app = core.App()
    stack = CdkTestingLabStack(app, "MyTestStack")

    # Generate CloudFormation template
    template = assertions.Template.from_stack(stack)

    # Assert that an S3 Bucket is created
    template.resource_count_is("AWS::S3::Bucket", 1)
```

---

### **Step 4: Run the Test Cases**  
Execute the tests:  
```sh
pytest
```

If successful, you will see:  
```
========================= test session starts =========================
collected 1 item

tests/test_cdk_testing_lab.py .                                  [100%]

========================== 1 passed in 0.34s ==========================
```

---

### **Step 5: Debugging & Improvements**  
- If the test fails, check error logs.  
- Modify the CDK stack and re-run tests.  
- Add more test cases for other AWS resources.  

---

### **Conclusion**  
This guide ensures **AWS infrastructure validation** before deployment, making deployments more reliable. 🚀