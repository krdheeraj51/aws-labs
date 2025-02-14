# Lab 15: AWS CloudFormation Lab: Nested Stacks
## Objective

This lab demonstrates Nested Stacks in AWS CloudFormation, allowing modular and reusable infrastructure deployment.

1. Understand Nested Stacks and their advantages.
2. Create a parent stack that references two child stacks.
3. Deploy a VPC, an EC2 instance, and an S3 bucket using nested stacks.

### Key Concept: Nested Stack
#### What is a Nested Stack?
A Nested Stack is a CloudFormation template inside another template. It allows you to:

- Reuse common infrastructure (like VPCs, security groups, etc.).
- Manage complex deployments with modular components.


## Prerequisites

Completion of [Lab 14(../Lab%2014/README.md)

## Lab Structure

- Parent Stack → Manages everything.
- Child Stack 1 → Creates an S3 Bucket.
- Child Stack 2 → Creates an EC2 Instance inside a VPC.
---

## Steps

### Steps for Nested Stack  in AWS CloudFormation

### 1. Go to AWS Console -> Navigate to AWS CloudFormation

- Log in to your AWS Console.
- In the search bar, type CloudFormation and click on the service.
- Click Create Stack → With new resources (standard).
---

### . Create CloudFormation Templates 

#### Step 1. Create the S3 Bucket template s3-bucket-stack.yaml

```
AWSTemplateFormatVersion: "2010-09-09"
Description: "Child Stack - S3 Bucket"

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "nested-stack-bucket-${AWS::AccountId}"

Outputs:
  S3BucketName:
    Description: "S3 Bucket Name"
    Value: !Ref MyS3Bucket
```
#### Step 2. Create the EC2 Nested Stack ec2-instance-stack.yaml
```
Resources:
  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: "Allow SSH and HTTP access"
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t2.micro
      ImageId: ami-085ad6ae776d8f09c  # Amazon Linux 2 (Change per region)
      SecurityGroupIds:
        - !Ref MySecurityGroup
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          yum update -y
          yum install -y httpd
          systemctl start httpd
          systemctl enable httpd
          echo "<html><h1>Nested Stack EC2 Running!</h1></html>" > /var/www/html/index.html

Outputs:
  EC2InstancePublicIP:
    Description: "Public IP of the EC2 Instance"
    Value: !GetAtt MyInstance.PublicIp
```
#### Step 3. Create the Parent Stack template parent-stack.yaml

```
Resources:
  # S3 Bucket Nested Stack
  S3BucketStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: "https://s3.amazonaws.com/YOUR_BUCKET/s3-bucket-stack.yaml"

  # EC2 Instance Nested Stack
  EC2InstanceStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: "https://s3.amazonaws.com/YOUR_BUCKET/ec2-instance-stack.yaml"

Outputs:
  S3BucketName:
    Description: "S3 Bucket Name"
    Value: !GetAtt S3BucketStack.Outputs.S3BucketName

  EC2PublicIP:
    Description: "Public IP of the EC2 Instance"
    Value: !GetAtt EC2InstanceStack.Outputs.EC2InstancePublicIP
```
3. Upload Child Templates to S3:

### 4. Upload the CloudFormation Template

- Before creating the parent stack, upload s3-bucket-stack.yaml and ec2-instance-stack.yaml to an S3 bucket.

1. Go to AWS S3 Console → Create a new bucket.
2. Upload both child templates.
3. Copy their S3 URLs and replace "https://s3.amazonaws.com/YOUR_BUCKET/..." in parent-stack.yaml.

---
5. Configure Stack Details

- Enter: 
    - Stack Name: **NestedStackLab**
    - KeyName: Select your existing Key Pair
- Click Next.
---
6. Verify Deployment
- Review the details to ensure everything is correct.
- Click Create stack.
---

7. Monitor Stack Creation

- Check Stack Status

- Go to CloudFormation Console → Stacks.
- Ensure Parent Stack and both Child Stacks show CREATE_COMPLETE.
✅ Verify S3 Bucket
    - Go to S3 Console → Find the bucket.
✅ Verify EC2 Instance
    - Go to EC2 Console → Copy Public IP.
    - Open in a browser: http://EC2_PUBLIC_IP.

---
9. Delete the CloudFormation Stack

- Go to AWS CloudFormation > Stacks.
- Select *CFNInItLab*.
- Click Delete and confirm.
---

### Key Takeaways:

✅ Nested Stacks → Modular CloudFormation templates.

✅ Reusability → Child stacks can be reused across projects.

✅ Simplified Management → Each stack handles its own resources.

✅ Dependency Handling → Parent stack controls the deployment order.

