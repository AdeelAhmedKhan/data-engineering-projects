# AWS Highly Available VPC with Public/Private Subnets and Endpoints

![VPC Architecture Diagram](architecture.png)

This repository provides step-by-step instructions to create a secure, highly available AWS Virtual Private Cloud (VPC) with public and private subnets, internet/NAT gateways, and VPC endpoints for S3 and DynamoDB.

## Contents

- `instruction.txt`: Detailed setup instructions for building the VPC architecture.
- `architecture.png`: Visual diagram of the VPC setup (referenced in the instructions).

## Overview

The guide walks you through:

1. **Creating a VPC** with a /16 CIDR block.
2. **Setting up public and private subnets** in different Availability Zones.
3. **Attaching an Internet Gateway** for public subnet internet access.
4. **Configuring route tables** for public and private subnets.
5. **Launching EC2 instances** in both subnets.
6. **Testing connectivity** between instances.
7. **Setting up a NAT Gateway** for outbound internet access from the private subnet.
8. **Creating VPC endpoints** for S3 and DynamoDB to allow private subnet access without using the NAT Gateway.

## Usage

1. Follow the steps in `instruction.txt` sequentially.
2. Refer to `architecture.png` for a visual reference.
3. Use the AWS Management Console or CLI as instructed.
4. Clean up resources after use to avoid unnecessary charges.

## Prerequisites

- AWS account with permissions to create VPC, subnets, EC2, IAM roles, and endpoints.
- Basic familiarity with AWS networking concepts.

## Security Notes

- Restrict security group rules to only necessary IPs and ports.
- Assign IAM roles to EC2 instances for least-privilege access to AWS services.

## License

This repository is provided for educational purposes.
