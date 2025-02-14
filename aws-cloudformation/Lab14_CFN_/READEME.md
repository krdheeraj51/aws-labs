# Lab 14: AWS CloudFormation Lab: Understanding cfn-init, cfn-signal, Fn::Sub, and CFN Hooks
## Objective

1. This lab will demonstrate how to use AWS CloudFormation Helper Scripts, including:

- cfn-init → Bootstraps and configures an EC2 instance.
- cfn-signal → Signals the completion of setup to CloudFormation.
- Fn::Sub → Helps in string substitution within the template.
- CloudFormation Hooks (AWS::CloudFormation::Hook) → Validates changes before stack deployment.

✅ Deploy an EC2 instance using CloudFormation.
✅ Use cfn-init to install software and configure the instance.
✅ Use cfn-signal to notify CloudFormation that instance setup is complete.
✅ Use Fn::Sub for better string formatting and referencing.
✅ Use AWS::CloudFormation::Hook to validate changes before deployment.


### Key Concept: 
- Metadata provides extra information about a CloudFormation template.
- AWS::CloudFormation::Interface is a special metadata type that helps improve the UI in the AWS CloudFormation console by:
    - Grouping parameters
    - Providing friendly labels
    - Adding helpful descriptions

## Prerequisites

Completion of [Lab 13(../Lab%2013/README.md)

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
AWSTemplateFormatVersion: "2010-09-09"
Description: "CloudFormation Lab - Using cfn-init, cfn-signal, Fn::Sub, and CFN Hooks"

Resources:
  MyEC2Instance:
    Type: AWS::EC2::Instance
    Metadata:
      AWS::CloudFormation::Init:
        config:
          packages:
            yum:
              httpd: []  # Install Apache
          files:
            /var/www/html/index.html:
              content: |
                <html>
                <head><title>CloudFormation Lab</title></head>
                <body><h1>Apache Installed via cfn-init</h1></body>
                </html>
              mode: "000644"
              owner: "apache"
              group: "apache"
          services:
            sysvinit:
              httpd:
                enabled: true
                ensureRunning: true  # Ensure Apache is running
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
          /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource MyEC2Instance --region ${AWS::Region}

  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: "Allow HTTP and SSH"
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0  # SSH Access (Use your IP for security)
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0  # HTTP Access

  MyValidationHook:
    Type: AWS::CloudFormation::Hook
    Properties:
      TypeName: "AWS::CloudFormation::PreCreateHook"
      Configuration:
        Message: "Validating stack before deployment"

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

- Stack name: Enter **CFN-Helper-Scripts-Lab**.
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
- Click on the stack **CFN-Helper-Scripts-Lab**.
- Navigate to the Resources tab.
    - Verify that the EC2 instance is created.
---
9. Delete the CloudFormation Stack

- Go to AWS CloudFormation > Stacks.
- Select **CFN-Helper-Scripts-Lab**.
- Click Delete and confirm.
---

### Key Takeaways:

✅ fn-init → Bootstraps the instance by installing and configuring software.

✅ cfn-signal → Notifies CloudFormation when EC2 setup is complete.

✅ Fn::Sub → Replaces placeholders dynamically in the template.

✅ CloudFormation Hooks → Validates changes before stack deployment.
