# Lab 5: Understanding DependsOn in AWS CloudFormation  

## Objective

This lab aims to provide hands-on experience in defining and deploying complex infrastructure using AWS CloudFormation. Participants will learn to:

1. Learn how **DependsOn** ensures resource creation order in AWS CloudFormation.
2. Deploy an **S3 bucket** and an **EC2 instance**, ensuring the bucket is created first.
3. Understand why **DependsOn** is necessary when there is no implicit dependency between resources.
4. Gain hands-on experience with defining **resource dependencies** in CloudFormation.

### Key Concept: DependsOn
In AWS CloudFormation, resources are usually created in parallel unless an explicit dependency is defined. The DependsOn attribute ensures that one resource is created before another.

In this lab:

1. We create an S3 bucket first.
2. The EC2 instance is deployed only after the bucket is successfully created.
3. This simulates a real-world scenario where an application instance depends on a pre-existing S3 bucket.

## Prerequisites

Completion of [Lab 4](../Lab%204/README.md)

## Steps

#### SSteps for implementing DependsOn:
1. Navigate to AWS CloudFormation

- Log in to your AWS Console.
- In the search bar, type CloudFormation and click on the service.
- Click Create Stack → With new resources (standard).


2. Create a CloudFormation Template **depends-on-template.yaml**:

3. Write the following YAML configuration:
```
Parameters:
  ImageId:
    Type: 'AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>'
    Default: '/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2'
    Description: SSM Parameter containing the desired AMI ID

Resources:
  MyS3Bucket:
    Type: 'AWS::S3::Bucket'  # Corrected resource type to S3::Bucket
    Description: An S3 bucket. # Added a description

  MyEC2Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      ImageId: !Ref ImageId
      KeyName: !Ref MyKeyName # Example: Assuming you have a KeyName parameter - you'll need to define this parameter as well
      InstanceType: t2.micro # Added a required InstanceType
    DependsOn: MyS3Bucket # The EC2 instance will be created after the S3 bucket
    Description: An EC2 instance. # Added a description
-   
```  
4. Upload the CloudFormation Template

- In the Specify template section, choose Upload a template file.
- Click Choose file and select your YAML file containing the template.
- Click Next.

5. Configure Stack Details

- Stack name: Enter a meaningful name, e.g., DependsOnLab.
- Parameters: If your template requires a Key Pair:
- Key Pair Name: Select an existing EC2 key pair from the dropdown (or create one in EC2 first).
- Click Next.

6.  Review and Create the Stack

- Review the stack details and ensure everything looks correct.
- Scroll down and check the I acknowledge that AWS CloudFormation might create IAM resources box (only if your template has IAM roles).
- Click Create stack.

7. Monitor Stack Creation

- In the CloudFormation > Stacks section, find your stack (DependsOnLab).
- Click on it and go to the Events tab.
- Observe that:
    - The S3 bucket (MyS3Bucket) is created first.
    - The EC2 instance (MyEC2Instance) is created only after the bucket is successfully deployed.
- This confirms that DependsOn is working correctly.

8. Delete Stack (Cleanup)

 - To remove all resources created by the stack:
 - Go to AWS CloudFormation → Stacks.
 - Select DependsOnLab.
 - Click Delete.
 - Confirm deletion and wait until the stack status changes to DELETE_COMPLETE.


### Key Learning Takeaways:

✅ **DependsOn in Action:** Ensures that the S3 bucket is created before the EC2 instance.
✅ **Observing the Execution Order:** The Events tab in CloudFormation shows the step-by-step resource creation sequence.
✅ **AWS CloudFormation Automation:** Deploying infrastructure without manual intervention.


