# Lab 2: Updating s3 Bucket Using a CloudFormation Template

## Objective

The objective of this lab is to create an AWS CloudFormation template that provisions an s3 bucket and demonstrates the foundational principles of Infrastructure as Code (IaC). By completing this lab, participants learn how to define AWS resources and manage them efficiently using CloudFormation.


## Prerequisites

Completion of [Lab 1](../Lab%201/README.md)

## Steps

1. Open the AWS Management Console and navigate to CloudFormation.
2. Create a new stack using the CloudFormation template (YAML/JSON).
3. Open a text editor and create a new file named **s3_bucket_template.yaml**.
4. Write the following YAML configuration:
```
Resources:
 AWSTemplateFormatVersion: '2010-09-09'
Description: AWS CloudFormation Template to create an S3 Bucket

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-unique-bucket-name  # Modify to a globally unique name
      VersioningConfiguration:
        Status: Enabled
```
##### Resources are mandatory. In this example, MyS3Bucket is the logical ID and identifies the s3 bucket resource to create.
4. Deploy the stack.
5. Monitor the Stack Creation:
    - Watch the stack creation progress. The status will change from **'CREATE_IN_PROGRESS'** to **'CREATE_COMPLETE'** upon successful creation of the bucket
5. Clean up the resources by deleting the stack.

