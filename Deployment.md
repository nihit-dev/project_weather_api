# Deployment

Deploying the Weather API Challenge application using AWS SAM (Serverless Application Model). The application will be using AWS S3 for file storage, AWS Lambda for processing data, and AWS RDS for data storage. The application exposes API endpoints using Api Gateway and Lambda function that fetch data from the RDS and return it to the user.

## Prerequisites

- AWS CLI installed and configured with your AWS account.
- AWS SAM CLI installed.
- Python 3.10 or higher installed.


## Architecture

The application will be using AWS S3 for file storage. When a file is uploaded to the S3 bucket, an AWS Lambda function will be triggered to process the data and store it in an AWS RDS instance. The application will expose two API endpoints via AWS API Gateway that fetch data from the RDS instance using a Lambda Function.

The application does not require a framework as it only has two simple API endpoints. AWS API Gateway can be used to document the APIs.

This is the most cost-effective and scalable solution. 

## Services Used
1. AWS S3 - For file storage.
2. AWS Lambda - For processing data.
3. AWS RDS - For data storage.
4. AWS API Gateway - For exposing API endpoints.
5. AWS CloudFormation - For managing the application resources.

## Deployment Steps
Deploying is also simple using the AWS SAM CLI. The SAM CLI will build the application and deploy it to AWS using CloudFormation.

1. **Build the SAM application**

    Use the SAM CLI to build our application:

    ```bash
    sam build
    ```

2. **Deploy the SAM application**

    Deploy your application:

    ```bash
    sam deploy --stack-name <your-stack-name>
    ```

3. **Cleanup**

   To delete the application:

   ```bash
   sam delete --stack-name <your-stack-name>
   ```
