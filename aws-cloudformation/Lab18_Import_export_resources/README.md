# Lab 18: AWS CloudFormation Lab: Understanding Import and Export of Resources
## Objective

1. Demonstrate how to export resources from one CloudFormation stack.
2. Show how to import those resources into another stack using Fn::ImportValue.
3. Understand the dependency management between different CloudFormation stacks.

- Exporter Stack: Creates and exports an S3 bucket name and VPC ID.
- Importer Stack: Imports the exported values to launch an EC2 instance in the specified VPC.

### Key Concept: Conditions in CloudFormation



## Prerequisites

Completion of [Lab 11](../Lab%2011/README.md)

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
AWSTemplateFormatVersion: "2010-09-09"
Description: "Exporter Stack - Creates and Exports S3 Bucket and VPC ID"

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "my-exported-bucket-${AWS::AccountId}"

  MyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16

Outputs:
  ExportedBucketName:
    Description: "Exports S3 bucket name"
    Value: !Ref MyS3Bucket
    Export:
      Name: "MyS3BucketName"

  ExportedVPCID:
    Description: "Exports VPC ID"
    Value: !Ref MyVPC
    Export:
      Name: "MyVPCID"

```  
### Exporter Stack
```
AWSTemplateFormatVersion: "2010-09-09"
Description: "Importer Stack - Uses exported values"

Parameters:
  KeyName:
    Type: String
    Description: "Name of an existing EC2 KeyPair"

Resources:
  ImportedEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t2.micro
      ImageId: !Ref AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
      NetworkInterfaces:
        - AssociatePublicIpAddress: true
          DeviceIndex: 0
          SubnetId: !ImportValue MyVPCID  # Importing VPC ID
      Tags:
        - Key: "ImportedResource"
          Value: "Yes"

Outputs:
  UsedS3Bucket:
    Description: "Imported S3 Bucket Name"
    Value: !ImportValue MyS3BucketName

```
4. Upload the CloudFormation Template

- In the Specify template section, choose Upload a template file.
- Click Choose file and select your YAML file containing the template.
- Click Next.
---
5. Configure Stack Details

- Stack name: Enter **ExporterStack**.
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
- Click on the stack **ExporterStack**.
- Navigate to the Resources tab.
    - Verify that the S3 bucket is created.
    - Verify that the EC2 instance is created.
- Go to the Outputs tab to see the S3 bucket name and EC2 instance ID.
---
9. Delete the CloudFormation Stack

- Go to AWS CloudFormation > Stacks.
- Select *ExporterStack*.
- Click Delete and confirm.
---

### Key Takeaways:

✅ Metadata (AWS::CloudFormation::Interface) enhances the CloudFormation UI experience.

✅ UserData installs Apache & PHP automatically.

✅ Security groups allow HTTP (80) and SSH (22) access.

✅ CloudFormation simplifies infrastructure deployment.
