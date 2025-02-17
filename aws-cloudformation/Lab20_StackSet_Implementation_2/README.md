# Lab 20: AWS CloudFormation : Demonstrating StackSet
## Objective

1. Understand AWS CloudFormation StackSets and their use cases.
2. Deploy a StackSet to create an S3 bucket in multiple AWS accounts or regions.
3. Use an IAM role for StackSet execution.
4. Deploy the StackSet from the AWS Management Console.


## Prerequisites
- AWS Management Console access.
- AWS Organizations with multiple accounts (for cross-account deployment).
- Required IAM permissions to create and manage StackSets.

## Steps

#### Steps for Outputs in AWS CloudFormation
1. Navigate to AWS CloudFormation

- Log in to your AWS Console.
---

2. Create an IAM Role for StackSet Administration

- Go to AWS IAM → Roles → Create Role
- Select AWS Service → CloudFormation
- Attach the AdministratorAccess policy.
- Name the role AWSCloudFormationStackSetAdministrationRole.
- Click Create Role.

3. Create an IAM Role for StackSet Execution
  - Go to AWS IAM → Roles → Create Role
  - Select Another AWS Account and enter your AWS Organization ID.
  - Attach the following JSON Policy:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "cloudformation:*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        }
    ]
}

```
- Name the role AWSCloudFormationStackSetExecutionRole.
- Click Create Role.
---

4. Create a CloudFormation Template **stackset-template.yaml**:

5. Write the following YAML configuration:
Save this YAML file as **stackset-template.yaml** in your GitHub repository
```
AWSTemplateFormatVersion: "2010-09-09"
Description: "StackSet to create an S3 bucket across multiple AWS accounts or regions"

Parameters:
  BucketNamePrefix:
    Type: String
    Default: stackset-demo-bucket
    Description: "Prefix for the S3 bucket name"

Resources:
  MyS3Bucket:
    Type: "AWS::S3::Bucket"
    Properties:
      BucketName: !Sub "${BucketNamePrefix}-${AWS::AccountId}-${AWS::Region}"
      Tags:
        - Key: "Project"
          Value: "StackSetDemo"

Outputs:
  BucketName:
    Description: "The S3 bucket name"
    Value: !Ref MyS3Bucket
```  
---
6. Deploy the StackSet from AWS Console
- Go to AWS CloudFormation → StackSets → Create StackSet.
- Upload the stackset-template.yaml file.
- Specify StackSet name as MyS3BucketStackSet.
- Choose Execution Role Name → Enter AWSCloudFormationStackSetExecutionRole.
- Deployment Options:
  - Choose Deploy to AWS Organizations (for multiple accounts)
  - Choose Deploy in multiple AWS regions
- Review & Deploy.
---
7. Verify Deployment
- Go to CloudFormation StackSets and check the deployment status.
- Navigate to S3 in multiple regions/accounts and confirm the bucket exists.
---
### Key Takeaways:

✅ StackSets enable multi-account, multi-region deployments.

✅ IAM roles are required for StackSet administration and execution.

✅ CloudFormation simplifies cross-account AWS resource management.
