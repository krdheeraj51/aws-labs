# Lab 6: Understanding DeletionPolicy in AWS CloudFormation  

## Objective

This lab aims to provide hands-on experience in defining and deploying complex infrastructure using AWS CloudFormation. Participants will learn to:

1. Learn how DeletionPolicy affects resource retention when a CloudFormation stack is deleted.
2. Deploy an S3 bucket with DeletionPolicy: Retain to prevent accidental deletion.
3. Observe the behavior when deleting the stack and verify that the bucket persists.
4. Gain hands-on experience in managing AWS resources safely with CloudFormation policies.

### Key Concept: DeletionPolicy
- By default, when a CloudFormation stack is deleted, all resources created within it are also deleted.
- The DeletionPolicy attribute prevents certain resources from being deleted.
- Available values:
    - Retain → The resource remains after stack deletion.
    - Snapshot → Takes a backup (e.g., for RDS databases).
    - Delete (default) → Removes the resource.


## Prerequisites

Completion of [Lab 5](../Lab%205/README.md)

## Steps

#### Steps for implementing DeletionPolicy:
1. Navigate to AWS CloudFormation

- Log in to your AWS Console.
- In the search bar, type CloudFormation and click on the service.
- Click Create Stack → With new resources (standard).


2. Create a CloudFormation Template **deletionPolicy-template.yaml**:

3. Write the following YAML configuration:
```
Resources:
  MyS3Bucket:
    Type: 'AWS::S3::Bucket'  # Corrected resource type to S3::Bucket
    Description: An S3 bucket. # Added a description
    DeletionPolicy: Retain   
```  
4. Upload the CloudFormation Template

- In the Specify template section, choose Upload a template file.
- Click Choose file and select your YAML file containing the template.
- Click Next.

5. Configure Stack Details

- Leave all settings default
- Click Next.

6.  Review and Create the Stack
- Review the stack details and ensure everything looks correct.
- Click Create stack.


7. Monitor Stack Creation

- In the CloudFormation > Stacks section, find your stack (DeletionPolicyLab).
- Click on it and go to the Resources tab.
- Ensure that MyS3Bucket is successfully created.
- Navigate to AWS S3 and confirm that the bucket exists.

8. Delete the CloudFormation Stack

 - Go to AWS CloudFormation → Stacks.
 - Select DeletionPolicyLab .
 - Click Delete.
 - Confirm deletion and wait until the stack status changes to DELETE_COMPLETE.

9. Verify Resource Retention

 - Wait for the stack deletion to complete.
 - Check that the stack is removed from AWS CloudFormation.
 - Navigate to AWS S3 → The bucket should still exist.
 - This is because DeletionPolicy: Retain prevented its deletion.

10. Manually Delete the S3 Bucket (Optional)

 - Go to AWS S3.
 - Click on the bucket name → Empty the bucket (if needed).
 - Click Delete bucket and confirm.


### Key Takeaways:

✅ **DeletionPolicy:** Retain ensures critical resources are not deleted.
✅ CloudFormation does NOT manage retained resources after stack deletion.
✅ Use this policy for persistent storage like S3 buckets and databases.


