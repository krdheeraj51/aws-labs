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
Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: "EC2 Configuration"
        Parameters:
          - InstanceType
      - Label:
          default: "Network Configuration"
        Parameters:
          - VPC
          - Subnet
    ParameterLabels:
      InstanceType:
        default: "EC2 Instance Type"

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

Resources:
  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: ami-085ad6ae776d8f09c  # Amazon Linux 2 AMI (Replace with valid AMI ID for your region)
      SecurityGroupIds:
        - !Ref MySecurityGroup
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          sudo yum update -y
          sudo amazon-linux-extras enable php8.0
          sudo yum install -y httpd php php-cli php-mysqlnd
          sudo systemctl start httpd
          sudo systemctl enable httpd
          echo "<?php phpinfo(); ?>" > /var/www/html/index.php

  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: "Allow HTTP and SSH access"
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0  # Allow SSH access (change for security)
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0  # Allow HTTP access

Outputs:
  WebsiteURL:
    Description: "PHP Web Server URL"
    Value: !Sub "http://${MyEC2Instance.PublicDnsName}"
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

✅ UserData installs Apache & PHP automatically.

✅ Security groups allow HTTP (80) and SSH (22) access.

✅ CloudFormation simplifies infrastructure deployment.
