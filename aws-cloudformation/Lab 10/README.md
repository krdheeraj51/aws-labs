# Lab 9: Understanding Conditions in AWS CloudFormation
## Objective

1. Learn how to use Conditions in AWS CloudFormation.
2. Deploy an S3 bucket and an EC2 instance, where:
  - The EC2 instance is only created if a condition is met (e.g., Environment is "Production").
      - Understand how to use conditions with parameters and intrinsic functions (!Equals, !If).


### Key Concept: Conditions in CloudFormation
- Conditions allow you to create resources only if certain conditions are met.
- They are useful for multi-environment deployments (e.g., Dev, QA, Prod).
- Conditions use intrinsic functions like !Equals, !If, !Not, !Or, and !And.

### Syntax 
```
Conditions:
  CreateEC2: !Equals [!Ref Environment, "Production"]
```
- This condition checks if Environment is "Production".

## Prerequisites

Completion of [Lab 9](../Lab%209/README.md)

## Steps

#### Steps for Outputs in AWS CloudFormation
1. Navigate to AWS CloudFormation

- Log in to your AWS Console.
- In the search bar, type CloudFormation and click on the service.
- Click Create Stack → With new resources (standard).


2. Create a CloudFormation Template **conditional-template.yaml**:

3. Write the following YAML configuration:
```
### CloudFormation Template: Demonstrating Conditions ###

Parameters:
  Environment:
    Type: String
    Description: "Specify the environment (Dev, QA, Production)"
    AllowedValues:
      - Dev
      - QA
      - Production
    Default: Dev

Conditions:
  CreateEC2: !Equals [!Ref Environment, "Production"]

Resources:
  MyS3Bucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      BucketName: !Sub "condition-demo-bucket-${AWS::AccountId}-${AWS::Region}"

  MyEC2Instance:
    Type: 'AWS::EC2::Instance'
    Condition: CreateEC2  # EC2 instance is created only if the condition is met
    Properties:
      ImageId: ami-0c55b159cbfafe1f0  # Update with a valid AMI ID for your region
      InstanceType: t2.micro
      KeyName: my-key-pair  # Replace with an actual key pair

Outputs:
  S3BucketName:
    Description: "Created S3 Bucket Name"
    Value: !Ref MyS3Bucket

  EC2InstanceStatus:
    Description: "EC2 instance created?"
    Value: !If [CreateEC2, "Yes, EC2 instance is created", "No, EC2 instance is skipped"]
   
```  
4. Upload the CloudFormation Template

- In the Specify template section, choose Upload a template file.
- Click Choose file and select your YAML file containing the template.
- Click Next.

5. Configure Stack Details

- Stack name: Enter **ConditionsLab**.
- Choose an Environment parameter value:
    - Dev: No EC2 instance will be created.
    - Production: EC2 instance will be created.
- Click Next.

6. Review and Create the Stack
- Review the details to ensure everything is correct.
- Click Create stack.


7. Monitor Stack Creation

- In the CloudFormation > Stacks section,
- Click on the stack **ConditionsLab**.
- Navigate to the Resources tab.
  - If Environment = Production: EC2 instance is created.
  - If Environment = Dev: EC2 instance is skipped.
- Check the Outputs tab for the EC2 creation status.

8. Validate the Outputs in AWS Console

- Check the S3 Bucket:
    - Go to S3 in the AWS Console.
- Check the EC2 Instance (if created):
    - Go to EC2 > Instances.
    - If **Production**, find the instance in the list.
    - If **Dev**, no instance should exist.

9. Delete the CloudFormation Stack

- Go to AWS CloudFormation > Stacks.
- Select ConditionsLab.
- Click Delete and confirm.


### Key Takeaways:

✅ Conditions allow conditional resource creation based on input parameters.

✅ This method helps deploy resources only when needed, reducing costs.

✅ You can use conditions with !If, !Equals, !Or, !And, and !Not.
