# Lab 4: Addding Multiple Resources

## Objective

This lab aims to provide hands-on experience in defining and deploying complex infrastructure using AWS CloudFormation. Participants will learn to:

1. **Design Multi-Resource Templates:** Create CloudFormation templates that define and provision multiple AWS resources, including but not limited to EC2 instances, security groups, VPCs, subnets, and internet gateways.
2. **Establish Resource Dependencies:** Understand and implement resource dependencies within CloudFormation templates to ensure resources are created in the correct order.
3. **Parameterize Templates:** Utilize parameters to make templates reusable and customizable, allowing for flexible configuration during stack creation.
4. **Utilize Intrinsic Functions:** Employ CloudFormation intrinsic functions (e.g., !Ref, !GetAtt, !Join) to dynamically reference resource properties and construct values.
5. **Implement Outputs:** Define outputs to retrieve key information about deployed resources, such as instance IDs, IP addresses, and DNS names.
6. **Deploy and Manage Stacks:** Deploy CloudFormation stacks, monitor their progress, and update or delete stacks as needed.
7. **Troubleshooting:** Learn to identify and resolve common CloudFormation deployment errors.


## Prerequisites

Completion of [Lab 3](../Lab%203/README.md)

## Steps

#### Steps for Adding Multiple Resources:
1. Set Up SSM Parameter Store:

- Navigate to the AWS Management Console and open the Systems Manager service.
- In the left navigation pane, choose "Parameter Store".
- Click "Create parameter".
- Define the parameter name (e.g., /dev/ec2/instanceType, /dev/ec2/ami). Use a hierarchical naming convention for better organization.
- Choose the parameter type (e.g., String, StringList, SecureString). For AMI IDs, use AWS::EC2::Image::Id.
- Enter the parameter value (e.g., t2.micro, ami-0abcdef1234567890).
- Optionally, add a description.
- Click "Create parameter". Repeat for all necessary parameters.

2. Create a CloudFormation Template **parameterExample-template.yaml**:

- Create a new CloudFormation template (YAML or JSON). 
- In the Parameters section:
    - Define a parameter that corresponds to your SSM parameter.
    - Set the Type to AWS::SSM::Parameter::Value<String> (or the appropriate type if it's not a string, like AWS::EC2::Image::Id).
    - Set the Default to the full path of your SSM parameter (e.g., /dev/ec2/instanceType). This is the crucial link.
    - Add a Description for clarity.
3. Write the following YAML configuration:
```
AWSTemplateFormatVersion: '2010-09-09'
Description: Deploys an EC2 instance with an Elastic IP and security groups.

Resources:
  # EC2 Instance : https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-instance.html#aws-resource-ec2-instance
  MyInstance:
    Type: 'AWS::EC2::Instance'
    Properties: 
      ImageId: ami-0a70b9d193ae8a799
      InstanceType: t2.micro
      KeyName: my-key-pair
      SecurityGroupIds: 
        - !Ref SSHSecurityGroup
        - !Ref ServerSecurityGroup

  # Elastic IP : https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-eip.html#aws-resource-ec2-eip
  MyEIP:
    Type: AWS::EC2::EIP
    Properties:
      InstanceId: !Ref MyInstance

  # Security Group for SSH Access : https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-securitygroup.html#aws-resource-ec2-securitygroup
  SSHSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable SSH access via port 22
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0

  # Security Group for Web Server Access
  ServerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow connections from specified CIDR ranges
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0  
  
```

4. Utilize Parameter in Resource Definitions:

- In the Resources section, use the !Ref intrinsic function to reference the parameter you defined. This will fetch the value from the SSM Parameter Store. For example: InstanceType: !Ref InstanceType

5. Deploy the CloudFormation Stack:

- In the AWS Management Console, go to CloudFormation.
- Click "Create stack".
- Upload your template.
- CloudFormation will automatically retrieve the values from the SSM Parameter Store during stack creation. You might see the resolved values in the CloudFormation console.
- Review and create the stack.

6. Monitor and Verify:

- Watch the stack creation progress. The status will change from **'CREATE_IN_PROGRESS'** to **'CREATE_COMPLETE'**
- Once the stack is created, check the resources. For example, verify the EC2 instance type in the EC2 console.



