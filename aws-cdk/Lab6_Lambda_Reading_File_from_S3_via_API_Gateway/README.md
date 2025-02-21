# **Lab 6: AWS Lambda Reading a File from S3 via API Gateway using AWS CDK**  

## **Objective**  
The goal of this lab is to:  
✅ **Create an S3 bucket** and store a sample file.  
✅ **Create an AWS Lambda function** that reads the file from S3.  
✅ **Set up an API Gateway** to trigger the Lambda function.  
✅ **Use IAM roles** to grant necessary permissions.  

---

## **Prerequisites**  
- AWS Account  
- AWS CLI installed and configured (`aws configure`)  
- Node.js installed  
- AWS CDK installed (`npm install -g aws-cdk`)  
- Python installed (Recommended: Python 3.8 or later)  
- An IDE such as VSCode  

---

## **Steps to Follow**  

### **Step 1: Setup Project Directory**  
1. Create a new folder and navigate into it:
   ```sh
   mkdir s3-lambda-api-lab
   cd s3-lambda-api-lab
   ```
2. Open the folder in VSCode:
   ```sh
   code .
   ```
3. Open the **terminal** in VSCode.

---

### **Step 2: Initialize AWS CDK App**  
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

---

### **Step 3: Define the S3 Bucket and Upload a Sample File**  
1. Open `s3_lambda_api_lab/s3_lambda_api_lab_stack.py` and modify it as follows:
```python
   import aws_cdk as cdk
   import aws_cdk.aws_s3 as s3
   import aws_cdk.aws_lambda as _lambda
   import aws_cdk.aws_iam as iam
   import aws_cdk.aws_apigateway as apigateway

   class S3LambdaApiLabStack(core.Stack):
       def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
           super().__init__(scope, id, **kwargs)

        # Create S3 bucket
        bucket = s3.Bucket(self, "MySampleBucket")

    # IAM Role for Lambda to access S3
        lambda_role = iam.Role(
            self, "LambdaS3Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
               ]
           )

    # Create Lambda function
        lambda_function = _lambda.Function(
            self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_cdk_lab.handler",
            code=_lambda.Code.from_asset("lambda"),
            role=lambda_role,
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "FILE_NAME": "sample.txt"
               }
           )

    # API Gateway to trigger Lambda
        api = apigateway.LambdaRestApi(
            self, "LambdaAPI",
            handler=lambda_function,
            proxy=True,
            deploy=True
           )
        
        items = api.root.add_resource("items")
        items.add_method("GET");

        cdk.CfnOutput(self, "BucketName", value=bucket.bucket_name)
```

---

### **Step 4: Create the Lambda Function**  
1. Inside the `s3-lambda-api-lab` directory, create a `lambda` folder:
   ```sh
   mkdir lambda
   ```
2. Create a Python file inside `lambda/` named **`lambda_function.py`** and add the following content:
```python
import boto3
import os

s3_client = boto3.client("s3")

def handler(event, context):
    bucket_name = os.environ["BUCKET_NAME"]
    file_name = os.environ["FILE_NAME"]

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        file_content = response["Body"].read().decode("utf-8")
        return {
            "statusCode": 200,
            "body": file_content
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error reading file: {str(e)}"
        }
  
```

---

### **Step 5: Bootstrap AWS Environment**  
Before deploying, bootstrap the AWS environment:
```sh
cdk bootstrap
```

---

### **Step 6: Deploy the Stack**  
1. Synthesize the CloudFormation template:
   ```sh
   cdk synth
   ```
2. Deploy the stack:
   ```sh
   cdk deploy
   ```

---

### **Step 7: Upload a Sample File to S3**  
Once the stack is deployed, **manually upload** a text file (`sample.txt`) to the S3 bucket.  
Alternatively, use the AWS CLI to upload the file:
```sh
echo "Hello from S3!" > sample.txt
aws s3 cp sample.txt s3://<BUCKET_NAME>/sample.txt
```
Replace `<BUCKET_NAME>` with the **output value** from the `cdk deploy` command.

---

### **Step 8: Test the API Gateway Endpoint**  
1. Retrieve the **API Gateway URL** from the CDK output.  
2. Open a browser or use **cURL** to test the Lambda function:
   ```sh
   curl <API_GATEWAY_URL>
   ```
   If everything is set up correctly, the API should return:
   ```json
   {
       "statusCode": 200,
       "body": "Hello from S3!"
   }
   ```

---

### **Step 9: Cleanup (Optional)**  
To remove all AWS resources created:
```sh
cdk destroy
```

---

## **Conclusion**  
In this lab, you have successfully:  
✅ Created an **S3 bucket** and stored a file  

✅ Created an **AWS Lambda function** that reads the file from S3  

✅ Configured **IAM Roles** for Lambda to access S3  

✅ Set up an **API Gateway** to trigger Lambda  

✅ Deployed everything using **AWS CDK**  

You now have a **serverless API** that reads files from S3! 🚀

