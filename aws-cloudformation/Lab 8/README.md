# Lab 8: Understanding Mappings in AWS CloudFormation

## Objective

1. Learn how to use Mappings in AWS CloudFormation to define key-value pairs for conditional configurations.
2. Deploy an EC2 instance that selects an AMI ID based on the region using Mappings.
3. Understand how Fn::FindInMap retrieves values dynamically from the Mapping section.
4. Gain hands-on experience deploying a stack via the AWS Console.

### Key Concept: Mappings in CloudFormation
- Mappings store key-value pairs that can be accessed using Fn::FindInMap.
- Useful for defining region-based AMI IDs, instance types, environment settings, etc.


## Prerequisites

Completion of [Lab 7](../Lab%207/README.md)

## Steps

#### Steps for Mappings in AWS CloudFormation
1. Navigate to AWS CloudFormation

- Log in to your AWS Console.
- In the search bar, type CloudFormation and click on the service.
- Click Create Stack → With new resources (standard).
---
2. Create a CloudFormation Template **mapping-template.yaml**:

3. Write the following YAML configuration:
```
#CloudFormation Template: Demonstrating Mappings ###

Mappings:
  RegionMap:
    us-east-1:
      AMI: ami-0c55b159cbfafe1f0  # Example AMI ID for us-east-1
    us-west-1:
      AMI: ami-0bdb828fd58c52235  # Example AMI ID for us-west-1
    eu-west-1:
      AMI: ami-047bb4163c506cd98  # Example AMI ID for eu-west-1

Resources:
  MyEC2Instance:
    Type: "AWS::EC2::Instance"
    Properties:
      ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", AMI]
      InstanceType: t2.micro
      KeyName: my-key-pair # Replace with an actual key pair
      Tags:
        - Key: Name
          Value: MappingLabInstance
   
```  
4. Upload the CloudFormation Template

- In the Specify template section, choose Upload a template file.
- Click Choose file and select your YAML file containing the template.
- Click Next.
---
5. Configure Stack Details

- Stack name: Enter **MappingsLab**.
- Click Next.
---
6.  Review and Create the Stack
- Review the details to ensure everything is correct.
- Click Create stack.
---
7. Monitor Stack Creation

- In the CloudFormation > Stacks section,
- Click on the stacck **MappingsLab**.
- In the Resources tab, confirm that MyEC2Instance is created.
- Navigate to EC2 Instances and verify that the instance is running.
---
8. Validate the Mapping Behavior

- Check the EC2 instance details in AWS Console.
- Look at the AMI ID used for the instance.
- Verify that it matches the correct AMI ID for the region as defined in the Mappings section.
---
9. Delete the CloudFormation Stack

- Go to AWS CloudFormation > Stacks.
- Select MappingsLab.
- Click Delete and confirm.
---
### Key Takeaways:

✅ Mappings allow region-specific or environment-specific configurations in CloudFormation.

✅ Fn::FindInMap retrieves values dynamically, reducing the need for complex logic.

✅ Mappings provide a more efficient way to manage configurations compared to parameters.

