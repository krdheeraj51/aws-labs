# Lab 11: Understanding Metadata – AWS::CloudFormation::Interface in AWS CloudFormation
## Objective

1. Learn how to use Metadata in CloudFormation.
2. Use AWS::CloudFormation::Interface to customize the CloudFormation console experience.
3. Deploy an S3 bucket and an EC2 instance, with a better UI for parameter selection.


### Key Concept: Conditions in CloudFormation
- Metadata provides extra information about a CloudFormation template.
- AWS::CloudFormation::Interface is a special metadata type that helps improve the UI in the AWS CloudFormation console by:
    - Grouping parameters
    - Providing friendly labels
    - Adding helpful descriptions

### Syntax 
```
Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: "EC2 Configuration"
        Parameters:
          - InstanceType
          - KeyName
    ParameterLabels:
      InstanceType:
        default: "EC2 Instance Type"
      KeyName:
        default: "SSH Key Name"
```
- Groups parameters logically under a friendly UI section.
- Adds meaningful labels for better user experience.
---
## Prerequisites

Completion of [Lab 10](../Lab%2011/README.md)

## Steps

#### Steps for Outputs in AWS CloudFormation
1. Navigate to AWS CloudFormation

- Log in to your AWS Console.
- In the search bar, type CloudFormation and click on the service.
- Click Create Stack → With new resources (standard).
---

2. Create a CloudFormation Template **metadata-template.yaml**:

3. Write the following YAML configuration:
```
Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: "EC2 Configuration"
        Parameters:
          - InstanceType
      - Label:
          default: "S3 Bucket Configuration"
        Parameters:
          - BucketName
    ParameterLabels:
      InstanceType:
        default: "EC2 Instance Type"
      BucketName:
        default: "S3 Bucket Name"

Parameters:
  InstanceType:
    Type: String
    Default: t2.micro
    Description: "Choose an EC2 instance type (e.g., t2.micro, t3.small, etc.)"
    AllowedValues:
      - t2.micro
      - t2.small
      - t3.micro
      - t3.small

  BucketName:
    Type: String
    Description: "Enter a unique name for the S3 bucket"

Resources:
  MyS3Bucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      BucketName: !Ref BucketName

  MyEC2Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: ami-085ad6ae776d8f09c  # Replace with a valid AMI ID for your region

Outputs:
  S3BucketName:
    Description: "Created S3 Bucket Name"
    Value: !Ref MyS3Bucket

  EC2InstanceId:
    Description: "Created EC2 Instance ID"
    Value: !Ref MyEC2Instance 
```  
4. Upload the CloudFormation Template

- In the Specify template section, choose Upload a template file.
- Click Choose file and select your YAML file containing the template.
- Click Next.
---
5. Configure Stack Details

- Stack name: Enter **MetadataLab**.
- Select appropriate values for:
    - InstanceType
    - KeyName (choose an existing key pair)
    - BucketName (enter a unique S3 bucket name)
- Click Next.
---
6. Review Changes under the Parameters section and Create the Stack
- Review the details to ensure everything is correct.
- Click Create stack.
---

7. Monitor Stack Creation

- In the CloudFormation > Stacks section,
- Click on the stack **MetadataLab**.
- Navigate to the Resources tab.
    - Verify that the S3 bucket is created.
    - Verify that the EC2 instance is created.
- Go to the Outputs tab to see the S3 bucket name and EC2 instance ID.
---
9. Delete the CloudFormation Stack

- Go to AWS CloudFormation > Stacks.
- Select *MetadataLab*.
- Click Delete and confirm.
---

### Key Takeaways:

✅ Metadata (AWS::CloudFormation::Interface) enhances the CloudFormation UI experience.

✅ ParameterGroups help organize parameters into sections.

✅ ParameterLabels provide more meaningful labels for better readability.


✅ This makes templates easier to understand for users deploying the stack
