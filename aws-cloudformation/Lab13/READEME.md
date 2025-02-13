# Lab 13: Understanding Metadata – Managing Packages, Users & Groups, Services, and Source Files
## Objective

1. This lab helps you understand how to use AWS CloudFormation to manage:

- Packages (installing software like httpd)
- Users and Groups (creating system users and assigning them to groups)
- Services (starting and enabling services like httpd)
- Source Files (copying configuration files from an S3 bucket)

1. By the end of this lab, you will:
2. Deploy an EC2 instance with Apache (httpd) installed.
3. Create a new Linux user and group on the instance.
4. Manage services (start and enable httpd).
5. Copy a sample configuration file from an S3 bucket to the instance.
6. Learn how to use the AWS::CloudFormation::Init feature.

### Key Concept: Conditions in CloudFormation
- Metadata provides extra information about a CloudFormation template.
- AWS::CloudFormation::Interface is a special metadata type that helps improve the UI in the AWS CloudFormation console by:
    - Grouping parameters
    - Providing friendly labels
    - Adding helpful descriptions

## Prerequisites

Completion of [Lab 12(../Lab%2012/README.md)

## Steps

#### Steps for Outputs in AWS CloudFormation
1.Open AWS S3 Console → Click Create Bucket (if needed).
- Upload a sample index.html file to the bucket.

1. Navigate to AWS CloudFormation

- Log in to your AWS Console.
- In the search bar, type CloudFormation and click on the service.
- Click Create Stack → With new resources (standard).
---

2. Create a CloudFormation Template **cfninit-template.yaml**:

3. Write the following YAML configuration:
```
Parameters:
  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: "Select an existing EC2 Key Pair for SSH access"

  S3BucketName:
    Type: String
    Description: "Enter the S3 bucket name containing index.html"

Resources:
  MyEC2Instance:
    Type: AWS::EC2::Instance
    Metadata:
      AWS::CloudFormation::Init:
        config:
          packages:
            yum:
              httpd: []  # Install Apache (httpd)
          groups:
            mygroup:
              gid: 6000  # Create a group with GID 6000
          users:
            myuser:
              uid: 2000  # Create a user with UID 2000
              groups:
                - mygroup
          services:
            sysvinit:
              httpd:
                enabled: true
                ensureRunning: true  # Ensure Apache service is running
          files:
            /var/www/html/index.html:
              source: !Sub "https://${S3BucketName}.s3.amazonaws.com/index.html"
              mode: "000644"
              owner: "apache"
              group: "apache"
    Properties:
      InstanceType: t2.micro
      ImageId: ami-085ad6ae776d8f09c  # Amazon Linux 2 AMI (Replace for your region)
      SecurityGroupIds:
        - !Ref MySecurityGroup
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          yum update -y
          yum install -y aws-cfn-bootstrap
          /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource MyEC2Instance --region ${AWS::Region}
          systemctl restart httpd

  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: "Allow HTTP and SSH"
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0  # SSH Access (For security, use your IP)
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0  # HTTP Access

Outputs:
  WebsiteURL:
    Description: "Access your website at"
    Value: !Sub "http://${MyEC2Instance.PublicDnsName}"
```  
4. Upload the CloudFormation Template

- In the Specify template section, choose Upload a template file.
- Click Choose file and select your YAML file containing the template.
- Click Next.
---
5. Configure Stack Details

- Stack name: Enter **CFNInItLab**.
- Select appropriate values for:
    - InstanceType
- Click Next.
---
6. Review Changes under the Parameters section and Create the Stack
- Review the details to ensure everything is correct.
- Click Create stack.
---

7. Monitor Stack Creation

- In the CloudFormation > Stacks section,
- Click on the stack **CFNInItLab**.
- Navigate to the Resources tab.
    - Verify that the EC2 instance is created.
- Go to the Outputs tab to see the S3 bucket name and EC2 instance ID.
---
9. Delete the CloudFormation Stack

- Go to AWS CloudFormation > Stacks.
- Select *CFNInItLab*.
- Click Delete and confirm.
---

### Key Takeaways:

✅ Metadata (AWS::CloudFormation::Interface) enhances the CloudFormation UI experience.

✅ UserData installs Apache & PHP automatically.

✅ Security groups allow HTTP (80) and SSH (22) access.

✅ CloudFormation simplifies infrastructure deployment.
