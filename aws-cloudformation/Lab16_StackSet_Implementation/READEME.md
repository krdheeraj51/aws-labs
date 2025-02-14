# Lab 16: AWS CloudFormation Lab: StackSet Demonstration
## Objective

This lab demonstrates Nested Stacks in AWS CloudFormation, allowing modular and reusable infrastructure deployment.

1. Understand StackSets and their benefits.
2. Deploy an S3 Bucket Stack using StackSets across multiple regions.
3. Learn how to create, update, and delete StackSets.

### Key Concept: Nested Stack
#### What is a StackSet?

**An AWS CloudFormation StackSet enables you to:**

  - Deploy CloudFormation stacks in multiple AWS accounts and regions.
  - Maintain consistent infrastructure across environments.
  - Use Administrator and Execution Roles to manage stack deployments.


## Prerequisites

Completion of [Lab 15(../Lab%2014/README.md)

## Lab Structure

- Administrator Account → Manages the StackSet.
- Target AWS Account(s) → Where the stacks will be deployed.
- IAM Roles → Grant permissions for StackSet execution.

---

## Steps

### Steps for StackSet Stack  in AWS CloudFormation

### 1. Go to AWS Console -> Navigate to AWS CloudFormation

- Log in to your AWS Console.
- In the search bar, type CloudFormation and click on the service.
- Click Create Stack → With new resources (standard).
---

### 2. Create and Deploy IAM Role Stack 

#### Step 1. Create IAM Role CloudFormation stackset-iam-roles.yaml.

**Note:** Creating a cloudformation for creating IAM role and attach **AWSCloudFormationStackSetAdministrationRole**

```
Resources:
  StackSetAdminRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: AWSCloudFormationStackSetAdministrationRole
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: cloudformation.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AdministratorAccess

  StackSetExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: AWSCloudFormationStackSetExecutionRole
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AWS::AccountId}:role/AWSCloudFormationStackSetAdministrationRole"
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AdministratorAccess

Outputs:
  StackSetAdminRoleArn:
    Description: "ARN of StackSet Administration Role"
    Value: !GetAtt StackSetAdminRole.Arn

  StackSetExecutionRoleArn:
    Description: "ARN of StackSet Execution Role"
    Value: !GetAtt StackSetExecutionRole.Arn
```
#### Step 2. Deployment Steps for IAM Role Template

- Open AWS CloudFormation Console → Click Create Stack.
- Select Upload a Template → Upload stackset-iam-roles.yaml.
- Click Next, enter Stack Name (e.g., StackSet-IAM-Roles).
- Click Next, leave default settings, and click Create Stack.
- Wait for CREATE_COMPLETE.

### 2. Create and Deploy IAM Role Stack 

#### Step 1. Create CloudFormation S3 bucket template s3-stackset-template.yaml

```
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "stackset-bucket-${AWS::Region}-${AWS::AccountId}"

Outputs:
  S3BucketName:
    Description: "The name of the created S3 bucket"
    Value: !Ref MyS3Bucket
```  
#### Step 2. Deployment Steps for S3 bucket Template
- Go to AWS CloudFormation Console → Click StackSets.
- Click Create StackSet → Select Upload a template file → Upload **s3-stackset-template.yaml**
- Click Next, enter StackSet Name **StackSetLab**
- Enter Parameters:
    - Administration Role → AWSCloudFormationStackSetAdministrationRole.
- Click Next, review the settings, and click Create StackSet.

### 3. Monitor Stack Instances to see S3 bucket different AWS accounts.


### 4. Delete the CloudFormation Stackset

### Key Takeaways:

✅ Nested Stacks → Modular CloudFormation templates.

✅ Reusability → Child stacks can be reused across projects.

✅ Simplified Management → Each stack handles its own resources.

✅ Dependency Handling → Parent stack controls the deployment order.

