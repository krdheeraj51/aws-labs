# Lab 20: AWS CloudFormation : Demonstrating Stack Policy
## Objective

This lab demonstrates how to implement and enforce a Stack Policy in AWS CloudFormation. Stack policies protect critical stack resources from accidental updates or deletions while allowing updates to other resources.


## Prerequisites
- AWS Management Console access.
- AWS Organizations with multiple accounts (for cross-account deployment).
- Required IAM permissions to create and manage StackSets.

## Key Concepts
- Stack Policy: Defines what updates are allowed or denied for specific stack resources.
- Deny Updates to Critical Resources: Prevent accidental changes to essential infrastructure (e.g., IAM roles, S3 buckets).
- Allow Safe Updates: Allow updates to other resources, such as EC2 instances.


## Steps

#### Steps for Outputs in AWS CloudFormation
1. Navigate to AWS CloudFormation

- Log in to your AWS Console.
---
2. Create the CloudFormation Stack Policy
This stack policy ensures that the DynamoDB table cannot be replaced or deleted when updating the CloudFormation stack.
```
{
  "Statement": [
    {
      "Effect": "Deny",
      "Action": [
        "Update:Replace",
        "Update:Delete"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceType": "AWS::DynamoDB::Table"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": "Update:*",
      "Principal": "*",
      "Resource": "*"
    }
  ]
}

```
#### Explanation:
- Deny Update:Replace & Update:Delete → Prevents table replacement and deletion.

- Applies only to AWS::DynamoDB::Table → Other resources can still be updated.

- Allows other updates (Update:*) → Ensures stack updates work except for deletion/replacement.

2. Create a CloudFormation Template **stackPolicy-template.yaml**:


```
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  MyDynamoDBTable:
    Type: 'AWS::DynamoDB::Table'
    Properties:
      TableName: MyDynamoDBStackPolicyDemo
      AttributeDefinitions:
        - AttributeName: ID
          AttributeType: S
      KeySchema:
        - AttributeName: ID
          KeyType: HASH
      BillingMode: PAY_PER_REQUEST
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain

```
---
3. Deploy the stack from AWS Console
- Click Create Stack → With new resources (standard)
- Upload the stackPolicy-template.yaml file.
---
4. Verify Deployment
- Go to CloudFormation StackSets and check the deployment status.
- Navigate to S3 in multiple regions/accounts and confirm the bucket exists.
---
5. Test the Stack Policy
- Test Case 1: Attempt to Delete the Table
  - Try deleting the stack.
  - Expected Result: The DynamoDB table will not be deleted due to DeletionPolicy: Retain.

- Test Case 2: Attempt to Update Table Name
  - Modify the CloudFormation template to change the table name.
  - Try updating the stack.
  - Expected Result: Update fails because the stack policy denies Update:Replace.

### Key Takeaways:

- UpdateReplacePolicy: Retain → Prevents accidental table replacement.
- DeletionPolicy: Retain → Ensures table retention even if the stack is deleted.
- Stack Policies can block updates at the resource level (AWS::DynamoDB::Table).
- This setup is useful for production environments to prevent data loss.

