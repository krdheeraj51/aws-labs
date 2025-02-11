# Lab 7: Understanding UpdateReplacePolicy in AWS CloudFormation

## Objective

This lab aims to provide hands-on experience in defining and deploying complex infrastructure using AWS CloudFormation. Participants will learn to:

1. Learn how **UpdateReplacePolicy** affects resource retention when an update triggers resource replacement.
2. **Deploy an S3 bucket with both DeletionPolicy: Retain and UpdateReplacePolicy:** Retain to ensure it is not lost during stack updates or deletions.
3. Modify the bucket name to trigger a resource replacement and observe that the existing bucket remains intact.
4. Gain hands-on experience with CloudFormation update behaviors to prevent accidental data loss.

### Key Concept: UpdateReplacePolicy
- AWS CloudFormation sometimes replaces a resource when its properties change (e.g., renaming an S3 bucket).
- UpdateReplacePolicy defines what happens to the old resource when it's replaced.
- Available values:
    - Retain → The old resource remains after being replaced.
    - Snapshot → Creates a backup before replacement (useful for databases).
    - Delete (default) → Deletes the old resource when replaced.


## Prerequisites

Completion of [Lab 6](../Lab%206/README.md)

## Steps

#### #### Steps for implementing UpdateReplacePolicy:
1. Navigate to AWS CloudFormation

- Log in to your AWS Console.
- In the search bar, type CloudFormation and click on the service.
- Click Create Stack → With new resources (standard).


2. Create a CloudFormation Template **updateReplace-template.yaml**:

3. Write the following YAML configuration:
```
### CloudFormation Template: Demonstrating UpdateReplacePolicy ###
Parameters: 
  BucketName:
    Type: String

Resources:
  MyS3Bucket:
    Type: 'AWS::S3::Bucket'
    Properties: 
      BucketName: !Ref BucketName
    Description: An S3 bucket with UpdateReplacePolicy set to Retain.
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain
-   
```  
4. Upload the CloudFormation Template

- In the Specify template section, choose Upload a template file.
- Click Choose file and select your YAML file containing the template.
- Click Next.

5. Configure Stack Details

- Stack name: Enter UpdateReplacePolicyLab.
- Click Next.
- BucketName Parameter: Enter a unique S3 bucket name (e.g., my-update-replace-bucket-123).
- Click Next.

6.  Review and Create the Stack
- Review the details to ensure everything is correct.
- Click Create stack.


7. Monitor Stack Creation

- In the CloudFormation > Stacks section, find your stack (UpdateReplacePolicyLab).
- Click on it and go to the Resources tab.
- Ensure that MyS3Bucket is successfully created.
- Navigate to AWS S3 and confirm that the bucket exists.

8. Trigger Resource Replacement

- Go to AWS CloudFormation > Stacks.
- Select UpdateReplacePolicyLab.
- Click Update → Edit Stack.
- Change the BucketName parameter (e.g., rename it to my-new-bucket-456).
- Click Next → Next → Update Stack.

9. Observe the Update Behavior

- Go to the CloudFormation > Stack Events tab.
- Notice that CloudFormation replaces the S3 bucket due to the name change.
- Navigate to AWS S3:
    - The old bucket is still there (because UpdateReplacePolicy: Retain).
    - The new bucket is created with the updated name.

10. Delete the CloudFormation Stack

 - Go to AWS CloudFormation → Stacks.
 - Select UpdateReplacePolicyLab .
 - Click Delete.
 - Confirm deletion and wait until the stack status changes to DELETE_COMPLETE.

11. Verify Resource Retention

- After deletion, check that the CloudFormation stack is removed.
- Navigate to AWS S3:
    - Both old and new buckets still exist because DeletionPolicy: Retain and UpdateReplacePolicy: Retain.
    - Manual cleanup is required to delete them.

10. Manually Delete the S3 Bucket (Optional)

 - Go to AWS S3.
 - Click on the bucket name → Empty the bucket (if needed).
 - Click Delete bucket and confirm.


### Key Takeaways:

✅ **UpdateReplacePolicy:** Retain prevents accidental deletion of old resources during an update.
✅ CloudFormation replaces the resource, but the original bucket remains safe.
✅ Use this policy for critical storage, databases, and resources that must not be lost on updates.

