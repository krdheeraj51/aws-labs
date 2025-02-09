# Lab 1: Creating s3 Bucket Using a CloudFormation Template

## Objective

Learn the basics of AWS CloudFormation by creating and managing a stack to create s3 Bukcet.

## Prerequisites

- AWS account
- Basic knowledge of AWS services

## Steps

1. Open the AWS Management Console and navigate to CloudFormation.
2. Create a new stack using the CloudFormation template (YAML/JSON).
3. Create the CloudFormation Template:
```
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties: {}
```
##### Resources are mandatory. In this example, MyS3Bucket is the logical ID and identifies the S3 bucket resource to create.
4. Deploy the stack and navigate to Amazon S3 to verify that your bucket has been created.
5. Clean up the resources by deleting the stack.

