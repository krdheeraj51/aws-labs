# **Lab 1: Creating an S3 Bucket Using AWS CDK (Python)**  

## **Objective**  
The objective of this lab is to create an Amazon S3 bucket using AWS CDK in Python. This lab demonstrates how to define AWS resources programmatically and manage them using Infrastructure as Code (IaC). By completing this lab, participants will learn:  

- How to set up an AWS CDK project in Python.  
- How to define and deploy an S3 bucket using AWS CDK.  
- How to synthesize and deploy CloudFormation templates using CDK commands.  

---

## **Prerequisites**  
- AWS CLI and AWS CDK installed on your machine.  
- An AWS account with the necessary IAM permissions.  
- Python 3.8+ installed.  

---

## **Steps**  

### **Step 1: Set Up Your AWS CDK Project**  
1. **Create a new project directory** and open it in your terminal:  
   ```
   mkdir aws-cdk-s3-lab && cd aws-cdk-s3-lab
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

### **Step 2: Define the S3 Bucket in CDK**  
1. Open `aws_cdk_s3_lab/aws_cdk_s3_lab_stack.py` in a text editor.  
2. Modify the file to define an S3 bucket:  
```
from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from constructs import Construct  # CDK v2 uses constructs module

class S3BucketStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):  # Use 'Construct' in CDK v2
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        s3.Bucket(
            self, "MyS3Bucket",
            bucket_name="my-cdk-bucket-example",
            # versioned=True
        )
```

---

### **Step 3: Bootstrap Your AWS Environment**  
If this is your first time using AWS CDK, run:  
```
cdk bootstrap
```
This sets up the necessary resources in your AWS account to support CDK deployments.

---

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
- Verify the bucket in the **AWS S3 console**.  

---

### **Step 7: Clean Up Resources**  
To delete the S3 bucket and all related resources, run:  
```
cdk destroy
```
This ensures that no unnecessary AWS resources remain in your account.

---

## **Conclusion**  
Congratulations! 🎉 You have successfully created and deployed an S3 bucket using AWS CDK in Python. This lab introduced foundational Infrastructure as Code (IaC) concepts and helped you understand AWS CDK workflows.

---
