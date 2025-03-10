# **AWS CloudFormation Lab: Cross-Stack Resource Sharing**  

## **📌 Objective:**  
In this lab, we will learn how to **share resources between two CloudFormation stacks** using **Export and ImportValue functions**.  

- **Stack 1:** Creates a **VPC and an S3 bucket**, then exports their values.  
- **Stack 2:** Imports the VPC ID and S3 bucket name from Stack 1 and creates an **EC2 instance inside the VPC**.  

---

## **🛠️ Step 1: Create the First Stack (Export Resources)**
This **CloudFormation template** creates a **VPC and an S3 bucket** and **exports their values** for other stacks to use.

### **`vpc-s3-export.yaml`**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  MyVPC:
    Type: 'AWS::EC2::VPC'
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: MySharedVPC

  MyS3Bucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      BucketName: my-cross-stack-demo-bucket

Outputs:
  VPCId:
    Description: The VPC ID
    Value: !Ref MyVPC
    Export:
      Name: MySharedVPCId

  S3BucketName:
    Description: The S3 Bucket Name
    Value: !Ref MyS3Bucket
    Export:
      Name: MySharedS3BucketName
```

### **🔹 Steps to Deploy Stack 1**
1. Open **AWS Management Console** → Go to **CloudFormation**.  
2. Click **Create stack → With new resources (standard)**.  
3. Upload the `vpc-s3-export.yaml` file.  
4. Click **Next**, name the stack `ExportStack`, and deploy it.  

---

## **🛠️ Step 2: Create the Second Stack (Import Resources)**
This **CloudFormation template** imports the **VPC ID and S3 bucket name** from Stack 1 and creates an **EC2 instance inside the VPC**.

### **`ec2-import.yaml`**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  MyEC2Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      ImageId: ami-0c55b159cbfafe1f0  # Replace with a valid AMI ID for your region
      InstanceType: t2.micro
      NetworkInterfaces:
        - AssociatePublicIpAddress: true
          DeviceIndex: 0
          SubnetId: 
            Fn::ImportValue: MySharedVPCId
      Tags:
        - Key: Name
          Value: MyCrossStackEC2

Outputs:
  InstanceId:
    Description: The EC2 instance ID
    Value: !Ref MyEC2Instance
```

### **🔹 Steps to Deploy Stack 2**
1. Open **AWS Management Console** → Go to **CloudFormation**.  
2. Click **Create stack → With new resources (standard)**.  
3. Upload the `ec2-import.yaml` file.  
4. Click **Next**, name the stack `ImportStack`, and deploy it.  

---

## **🛠️ Step 3: Verify the Cross-Stack Dependency**
### **✅ Validate the Exports**
1. Go to **AWS CloudFormation** → Click **Exports** (on the left panel).  
2. Ensure you see **MySharedVPCId** and **MySharedS3BucketName** exported.  

### **✅ Validate Stack 2 Resources**
1. Go to **EC2 Console** → Check if the **EC2 instance** was launched.  
2. Go to **S3 Console** → Ensure the **bucket exists**.  

---

## **🎯 Key Takeaways**
- **Cross-stack resource sharing** allows efficient resource reuse.  
- **`Export` and `ImportValue` functions** enable stacks to communicate.  
- This approach helps manage **modular infrastructure** and avoids duplication.  

🚀 **This lab demonstrates how CloudFormation stacks can work together!**