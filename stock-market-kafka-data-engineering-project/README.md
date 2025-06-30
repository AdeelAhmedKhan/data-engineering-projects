# Stock Market Kafka Data Engineering Project

This project demonstrates an end-to-end data engineering pipeline using Apache Kafka, AWS S3, AWS Glue, and AWS Athena for real-time stock market data ingestion, storage, and analytics.

## Architecture

The following diagram illustrates the high-level architecture of the pipeline:

![Architecture Diagram](architecture.jpg)

**Components:**
- **Kafka Producer:** Sends stock market data to a Kafka topic.
- **Kafka Broker:** Manages the topic and message distribution.
- **Kafka Consumer:** Consumes messages for further processing or storage.
- **AWS S3:** Stores raw or processed data.
- **AWS Glue:** Crawls S3 data and creates a schema for analytics.
- **AWS Athena:** Enables SQL-based analytics on the data stored in S3.

## Prerequisites

- AWS account with permissions for EC2, S3, Glue, and Athena.
- EC2 instance (Amazon Linux recommended).
- Security group allowing inbound access on ports 22 (SSH), 9092 (Kafka), and 2181 (ZooKeeper).
- AWS CLI installed and configured.
- Java 8+ installed on EC2.

## Setup Instructions

1. **Connect to EC2 Instance**
   - SSH into your EC2 instance using your PEM key.

2. **Install Java and Download Kafka**
   - Install Java 8.
   - Download and extract Kafka binaries.

3. **Start ZooKeeper and Kafka**
   - Start ZooKeeper in one terminal.
   - Edit `config/server.properties` to set `advertised.listeners` to your EC2 public IP.
   - Start Kafka server in another terminal.

4. **Create Kafka Topic**
   - Create a topic (e.g., `practice`) using Kafka CLI tools.

5. **Start Producer and Consumer**
   - Use Kafka console producer to send messages.
   - Use Kafka console consumer to receive messages.

6. **Store Data in S3**
   - Create an S3 bucket and IAM user with access.
   - Configure AWS CLI and upload data to S3.

7. **Data Analytics with Glue and Athena**
   - Create a Glue crawler to catalog S3 data.
   - Use Athena to run SQL queries on the data.

## Usage

- Follow the detailed step-by-step instructions in `command_kafka.txt` for setup and operations.
- Modify and extend the pipeline as needed for your data engineering use case.

## References

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [AWS Glue Documentation](https://docs.aws.amazon.com/glue/)
- [AWS Athena Documentation](https://docs.aws.amazon.com/athena/)
- Project inspiration: [YouTube Video - Stock Market Data Engineering Pipeline with Kafka & AWS](https://www.youtube.com/) <!-- Replace with actual video URL if available -->

---

For any issues or contributions, please open an issue or pull request in this repository.
