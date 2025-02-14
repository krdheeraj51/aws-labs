# Lab 17: AWS CloudFormation Lab: Using UserData from S3 to Launch an EC2 Instance with PHP Setup
## Objective

1. Store a UserData script in an S3 bucket that installs PHP and Apache on an EC2 instance.
2. Retrieve and execute the script from S3 when launching the EC2 instance.
3. Use CloudFormation Outputs to display whether Apache is running.


### Key Concept: Conditions in CloudFormation
- Metadata provides extra information about a CloudFormation template.
- AWS::CloudFormation::Interface is a special metadata type that helps improve the UI in the AWS CloudFormation console by:
    - Grouping parameters
    - Providing friendly labels
    - Adding helpful descriptions

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
Resources:
  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: "Allow HTTP and SSH"
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t2.micro
      SecurityGroups:
        - !Ref MySecurityGroup
      ImageId: ami-085ad6ae776d8f09c
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          aws s3 cp s3://application-13-demo/userdata.sh /tmp/userdata.sh
          chmod +x /tmp/userdata.sh
          /tmp/userdata.sh
Outputs:
  ApacheStatus:
    Description: "Apache Service Status"
    Value: !Sub |
      The status of Apache is stored in /tmp/apache_status.txt on your EC2 instance.  
#      Run the following command to check:  
#      ssh -i <YourKey.pem> ec2-user@${MyEC2Instance.PublicIp} 'cat /tmp/apache_status.txt'
   
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
