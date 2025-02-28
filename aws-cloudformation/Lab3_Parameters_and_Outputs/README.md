# Lab 3: Parameters and Outputs

## Objective

This lab aims to provide hands-on experience with managing configuration values in AWS CloudFormation using SSM Parameters.  Participants will:

1. **Understand SSM Parameters:** Grasp the concept of SSM parameters and their benefits in managing configuration data separately from CloudFormation templates.
2. **Integrate SSM Parameters in Templates:** Learn to incorporate SSM parameters within CloudFormation templates to dynamically fetch configuration values.
3. **Ensure Dynamic Value Fetching:** Implement mechanisms to ensure CloudFormation retrieves the most up-to-date SSM parameter values during stack creation and updates, enabling dynamic configuration management.
4. **Practice Best Practices:** Understand and apply best practices for using SSM parameters with CloudFormation, including naming conventions and parameter organization.


## Prerequisites

Completion of [Lab 2](../Lab%202/README.md)

## Steps

#### Steps for Implementing Parameter Theory in AWS CloudFormation using SSM:
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
Parameters:
  InstanceType:
    Type: 'AWS::SSM::Parameter::Value<String>'
    Default: '/dev/ec2/instanceType'
    Description: SSM Parameter containing the desired instance type

  AMI:
    Type: 'AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>'
    Default: '/dev/ec2/ami'
    Description: SSM Parameter containing the AMI ID

Resources:
  MyEC2Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      InstanceType: !Ref InstanceType  # This line was missing!
      ImageId: !Ref AMI
      # KeyName: !Ref MyKeyName # Example: Assuming you have a KeyName parameter - Uncomment and define MyKeyName if needed
      Tags:
        - Key: Name
          Value: MySSMParameterInstance

# MyKeyName: # Example KeyPair parameter (not from SSM) - Uncomment if you want to use a KeyPair
#   Type: AWS::EC2::KeyPair::KeyName
#   Description: Name of an existing EC2 KeyPair to enable SSH access

Outputs:
  InstanceId:
    Value: !Ref MyEC2Instance
    Description: Instance ID of the created EC2 instance
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
- You can also check the stack outputs for values that might be derived from the SSM parameters.


