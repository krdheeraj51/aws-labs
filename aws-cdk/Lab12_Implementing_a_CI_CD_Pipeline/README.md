# **Lab: Implementing a CI/CD Pipeline using AWS CDK and GitHub**  
This lab demonstrates how to set up a **CI/CD pipeline using AWS CDK**, AWS CodePipeline, AWS CodeBuild, and GitHub as the source repository.  

---

## **Objective**  
In this lab, we will:  
✅ Set up a **GitHub repository** to store the source code.  
✅ Create a **CI/CD pipeline** in **AWS CodePipeline** using AWS CDK.  
✅ Automate build and deployment of an **AWS Lambda function** using **AWS CodeBuild**.  
✅ Ensure every commit in GitHub triggers an automatic deployment.

---

## **Prerequisites**  
- An **AWS account** with necessary permissions.  
- **AWS CLI installed** and configured.  
- **AWS CDK installed** (`npm install -g aws-cdk`).  
- **Python 3.8+ installed**.  
- **Git installed and configured** with a GitHub account.  
- **GitHub Personal Access Token** with repository read access.  

---

## **Step 1: Create a GitHub Repository**  
1. **Go to GitHub** and create a new repository:
   - Repository name: **cdk-cicd-pipeline**  
   - Make it **public** or **private** as needed.  
   - Do not initialize with a README or `.gitignore`.  

2. **Clone the repository locally**:
   ```sh
   git clone https://github.com/your-github-username/cdk-cicd-pipeline.git
   cd cdk-cicd-pipeline
   ```

---

## **Step 2: Initialize an AWS CDK Project**  
1. Initialize a new AWS CDK project:
   ```sh
   cdk init app --language python
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Add **CDK dependencies**:
   ```sh
   pip install aws-cdk-lib constructs
   ```

---

## **Step 3: Create CI/CD Pipeline using AWS CDK**  
### **Modify `cdk_cicd_pipeline/cdk_cicd_pipeline_stack.py`**
Replace the contents with:  

```python
from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions,
    aws_codebuild as codebuild,
    aws_lambda as _lambda,
    SecretValue
)
from constructs import Construct

class CicdPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Lambda Function
        lambda_function = _lambda.Function(
            self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("lambda")
        )

        # Create a CodeBuild Project
        build_project = codebuild.PipelineProject(
            self, "BuildProject",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "install": {
                        "runtime-versions": {"python": "3.8"},
                        "commands": ["pip install -r requirements.txt"]
                    },
                    "build": {
                        "commands": ["echo 'Building the package'"]
                    }
                },
                "artifacts": {"files": ["**/*"]}
            })
        )

        # GitHub Source
        source_artifact = codepipeline.Artifact()
        build_artifact = codepipeline.Artifact()
        oauth_token = SecretValue.secrets_manager('github_cicd_accesss_secure_token')

        source_action = cpactions.GitHubSourceAction(
            action_name="GitHub_Source1",
            owner="krdheeraj51",
            repo="cdk-cicd-pipeline",
            oauth_token=oauth_token,
            output=source_artifact,
            branch="main",
            trigger=cpactions.GitHubTrigger.WEBHOOK
        )

        # CodeBuild Action
        build_action = cpactions.CodeBuildAction(
            action_name="Build",
            project=build_project,
            input=source_artifact,
            outputs=[build_artifact]
        )

        # Deploy Action
        deploy_action = cpactions.LambdaInvokeAction(
            action_name="DeployLambda",
            lambda_=lambda_function
        )

        # Define CodePipeline
        pipeline = codepipeline.Pipeline(
            self, "Pipeline",
            stages=[
                codepipeline.StageProps(stage_name="Source", actions=[source_action]),
                codepipeline.StageProps(stage_name="Build", actions=[build_action]),
                codepipeline.StageProps(stage_name="Deploy", actions=[deploy_action])
            ]
        )
```

---

## **Step 4: Add Lambda Function Code**
1. Create a `lambda/` directory inside the project:
   ```sh
   mkdir lambda
   ```
2. Inside `lambda/`, create a file called `index.py`:
   ```python
   def lambda_handler(event, context):
       return {"statusCode": 200, "body": "Deployment Successful!"}
   ```
3. Add `requirements.txt` for dependencies:
   ```sh
   touch requirements.txt
   ```

---

## **Step 5: Configure GitHub Token in CDK Context**  
1. **Generate a GitHub Personal Access Token**:
   - Go to **GitHub → Settings → Developer Settings → Personal Access Tokens**.
   - Generate a **classic token** with **repo read access**.

2. **Store the token in secret Manager**:
- Navigate to AWS Secrets Manager:

      - Open the AWS Management Console and navigate to the AWS Secrets Manager service.
      - Create a New Secret:
      - Click Store a new secret.
---

## **Step 6: Commit Code to GitHub**
1. Initialize Git and commit:
   ```sh
   git add .
   git commit -m "Initial commit for CDK CI/CD pipeline"
   ```
2. Push to GitHub:
   ```sh
   git push origin main
   ```

---

## **Step 7: Deploy the CI/CD Pipeline**  
1. Bootstrap the AWS environment:
   ```sh
   cdk bootstrap
   ```
2. Synthesize the CloudFormation template:
   ```sh
   cdk synth
   ```
3. Deploy the stack:
   ```sh
   cdk deploy
   ```

---

## **Step 8: Verify CI/CD Pipeline**
1. **Go to AWS CodePipeline Console**.
2. Locate the **pipeline created by CDK**.
3. Trigger a **new commit** in GitHub and verify that:
   - CodePipeline pulls the latest code.
   - CodeBuild executes the build.
   - Lambda is updated automatically.

---

## **Step 9: Cleanup Resources**
To delete all AWS resources:
```sh
cdk destroy
```

---

## **Conclusion**  
✅ Set up a **GitHub repository** to store the source code. 

✅ Created an **AWS CDK stack** for CI/CD automation.  

✅ Configured **AWS CodePipeline and CodeBuild**.  

✅ Deployed an **AWS Lambda function automatically** upon code changes.  

Now, every time you **push changes** to the GitHub repository, AWS CodePipeline will **automatically build and deploy the updates**! 🚀  
