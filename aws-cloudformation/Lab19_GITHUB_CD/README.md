# Lab 19: AWS CloudFormation : Automating Deployment with GitHub Push
## Objective

1. Demonstrate CI/CD with GitHub Actions and AWS CloudFormation.
2. Automatically deploy a CloudFormation stack when code is pushed to GitHub.
3. Use AWS CLI within GitHub Actions to trigger CloudFormation stack creation or updates.


### Architecture Overview
- GitHub Repository: Stores the CloudFormation template.
- GitHub Actions Workflow: Triggers deployment when a push is made to the main branch.
- AWS CloudFormation: Creates and manages AWS resources based on the template.

## Prerequisites

Completion of [Lab 18](../Lab%2011/README.md)

## Steps

#### Steps for Outputs in AWS CloudFormation
1. Navigate to AWS CloudFormation

- Log in to your AWS Console.
---

2. Create an IAM Role for GitHub Actions
- Before automating deployment, create an IAM role that allows GitHub to interact with AWS.
##### IAM Role Policy (JSON)
- Go to IAM → Policies → Create Policy
- Choose JSON and paste:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cloudformation:CreateStack",
                "cloudformation:UpdateStack",
                "cloudformation:DescribeStacks",
                "s3:CreateBucket",
                "s3:PutObject",
                "ec2:*"
            ],
            "Resource": "*"
        }
    ]
}

```
- Name the policy *GitHubCloudFormationPolicy*.
- Go to IAM → Roles → Create Role
- Choose AWS Service → EC2, attach the above policy, and name it GitHubCloudFormationRole.
- Copy the Role ARN, as we will use it in GitHub Actions.
---
3. Store AWS Credentials in GitHub Secrets

- Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret.
- Create the following secrets:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION (e.g., us-east-1)
---

4. Create a CloudFormation Template **cloudformation-template.yaml**:

5. Write the following YAML configuration:
Save this YAML file as **cloudformation-template.yaml** in your GitHub repository
```

Parameters:
  InstanceType:
    Type: String
    Default: t2.micro

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "github-deployment-bucket-${AWS::AccountId}"

  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: !Ref AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
      Tags:
        - Key: "DeployedBy"
          Value: "GitHubActions"

Outputs:
  BucketName:
    Description: "S3 Bucket Created"
    Value: !Ref MyS3Bucket
  InstanceID:
    Description: "EC2 Instance ID"
    Value: !Ref MyEC2Instance

```  
---
6. Create a GitHub Actions Workflow
- Save this file as .github/workflows/deploy-cloudformation.yml in your repo.
```
name: Deploy to AWS CloudFormation

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Deploy CloudFormation Stack
        run: |
          aws cloudformation deploy \
            --stack-name MyGitHubDeploymentStack \
            --template-file cloudformation-template.yaml \
            --capabilities CAPABILITY_NAMED_IAM
```
7. Test the Deployment
- Push the CloudFormation template and workflow files to GitHub.
- Go to GitHub Actions (Actions tab in the repository).
- Check if the workflow runs successfully.
- Go to AWS CloudFormation and verify the deployed stack (**MyGitHubDeploymentStack**).
---

8. Delete the CloudFormation Stack

- Go to AWS CloudFormation > Stacks.
- Select *MyGitHubDeploymentStack*.
- Click Delete and confirm.
---

### Key Takeaways:

✅ Automated deployments using GitHub Actions and AWS CloudFormation

✅ IAM permissions enable GitHub to interact with AWS securely

✅ CloudFormation template manages AWS infrastructure with ease
