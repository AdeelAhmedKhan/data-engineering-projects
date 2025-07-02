🔷 STEP 1: Create the VPC

Refer to the architecture diagram (`architecture.png`) for a visual overview of the setup.

Let’s begin.

🛠 VPC Settings:
Name: virtual-private-cloud

IPv4 CIDR block: 10.0.0.0/16

Tenancy: Default

This will give us:

IP Range: 10.0.0.1 – 10.0.255.254

Available IPs: 65,536


🔷 STEP 2: Create Subnets (Public & Private)
We'll create two subnets in different Availability Zones (recommended for high availability):

📍 Subnet A (Public)
  - Name: Public-Subnet-A
  - CIDR: 10.0.0.0/24
  - AZ: Select one (e.g., ap-south-1a)
  - Auto-assign public IP: Enabled

📍 Subnet B (Private)
  - Name: Private-Subnet-B
  - CIDR: 10.0.1.0/24
  - AZ: Select a different one (e.g., ap-south-1b)
  - Auto-assign public IP: Disabled


🔷 STEP 3: Create and Attach the Internet Gateway (IGW)
Now let’s make your public subnet internet accessible.

🛠 Tasks:
1. Go to VPC Dashboard → Internet Gateways
2. Click "Create internet gateway"
3. Name it: My-IGW
4. After creation, select the IGW → Actions → Attach to VPC
5. Choose your VPC (virtual-private-cloud) and attach


🔷 STEP 4: Create Route Tables (Public & Private)
We’ll create two route tables:

🔹 1. Public Route Table
  - Name: Public-Route-Table
  - Associate with Public-Subnet-A
  - Add route: `0.0.0.0/0` → Internet Gateway (IGW)

🔹 2. Private Route Table
  - Name: Private-Route-Table
  - Associate with Private-Subnet-B
  - (No internet route yet; will add NAT Gateway later)


🔷 STEP 5: Launch EC2 Instances (Public & Private)
We’ll launch 2 EC2 instances:

1. Public EC2 Instance:
   - Subnet: Public-Subnet-A
   - Auto-assign public IP: Enabled
   - Security Group: Allow SSH (port 22) from your IP, ICMP (ping) from Public-Subnet-A and Private-Subnet-B
   - Key Pair: Create/download a key pair (e.g., vpc-public-ec2.pem)

2. Private EC2 Instance:
   - Subnet: Private-Subnet-B
   - Auto-assign public IP: Disabled
   - Security Group: Allow SSH (port 22) from Public-Subnet-A, ICMP (ping) from Public-Subnet-A and Private-Subnet-B
   - Key Pair: Use the same or a different key pair


🔷 STEP 6: Test SSH & Ping Between EC2 Instances
✅ 1. SSH into Public EC2:
```bash
chmod 400 vpc-public-ec2.pem
ssh -i "vpc-public-ec2.pem" ec2-user@<PUBLIC-IP-of-Public-EC2>
```
If you’re in, you're good!

✅ 2. Ping Private EC2 from Public EC2:
```bash
ping <Private-IP-of-Private-EC2>
```
If ping works, your subnets and security groups are configured correctly.

✅ 3. (Optional) SSH into Private EC2 from Public EC2:
```bash
ssh -i "vpc-public-ec2.pem" ec2-user@<Private-IP-of-Private-EC2>
```
This requires the private EC2's security group to allow SSH from the public subnet.


🔷 STEP 7: Set Up NAT Gateway (for Private EC2 → Internet)
Since your Private EC2 has no public IP, it can’t access the internet — but it can through a NAT Gateway.

✅ NAT Gateway Setup (Step-by-Step):
1. Allocate an Elastic IP:
   - Go to EC2 Dashboard → Elastic IPs
   - Click "Allocate Elastic IP" (keep all settings default)
2. Create NAT Gateway:
   - Go to VPC Dashboard → NAT Gateways
   - Click "Create NAT Gateway"
   - Name: My-NAT-Gateway
   - Subnet: Public-Subnet-A (very important)
   - Elastic IP: Select the one you just allocated
   - Click "Create NAT Gateway"
   - Wait until its status is "Available"
3. Update Private Route Table:
   - Go to VPC Dashboard → Route Tables
   - Select Private-Route-Table
   - Add route: `0.0.0.0/0` → NAT Gateway

> **Why?**
> The NAT Gateway allows private subnet instances to access the internet (for updates, etc.) without exposing them to inbound internet traffic. The NAT Gateway must be in a public subnet so it can reach the internet via the IGW.


🔷 STEP 8: Create VPC Endpoints for S3 & DynamoDB
This step lets your Private EC2 access AWS services like S3 and DynamoDB without using the NAT Gateway — reducing cost and increasing security.

🔹 For S3:
  - Service: com.amazonaws.<region>.s3
  - VPC: virtual-private-cloud
  - Route table: Private-Route-Table
  - Type: Gateway
  - Click "Create endpoint"

🔹 For DynamoDB:
  - Service: com.amazonaws.<region>.dynamodb
  - VPC: virtual-private-cloud
  - Route table: Private-Route-Table
  - Type: Gateway
  - Click "Create endpoint"


🔄 After Setup, Test on Private EC2:
SSH into Private EC2 (use the Public EC2 as a jump host if needed) and run:

**Test S3:**
1. Configure AWS CLI with access key or assign an IAM role with S3 access to the instance.
2. Run:
```bash
aws s3 ls s3://your-bucket-name
```

**Test DynamoDB:**
1. Ensure IAM role or credentials allow DynamoDB access.
2. Run:
```bash
aws dynamodb list-tables
```

> **Note:**
> - Ensure your EC2 instance has an IAM role with S3/DynamoDB access, or configure credentials with `aws configure`.
> - The VPC endpoint allows network access, but IAM permissions are still required.
> - For best security, restrict security group rules to only necessary IPs and ports.
> - Always clean up resources after testing to avoid unnecessary charges.

✅ **You have now set up a secure, highly available VPC with public and private subnets, internet/NAT gateways, and VPC endpoints for AWS services.**