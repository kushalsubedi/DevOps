📂 DocuMind
DocuMind is a serverless document management application that leverages AI to provide summarization and title suggestion for your uploaded text files. The entire infrastructure is managed with Terraform.

## Features
File Management: Upload files directly to a secure Amazon S3 bucket.

Automated File Organization: Automatically sorts uploaded files into type-specific folders (e.g., /images, /documents) in the main storage bucket.

Core Operations: List, download, rename, and delete your files.

AI Summarization: Right-click any text file to generate a concise summary using the Hugging Face Inference API.

AI Title Suggestion: Automatically suggest a new, relevant title for your documents.

Modern UI: A clean, aesthetic user interface with a right-click context menu for easy access to all actions.

## Tech Stack & Architecture
This project is built with a serverless-first approach using Infrastructure as Code.

Frontend:

HTML5

CSS3

Vanilla JavaScript (ES6+ async/await)

Backend (AWS Serverless):

API Gateway: Provides the REST API endpoints for all frontend operations.

AWS Lambda: Python functions that handle the business logic (file operations, calling AI models, sorting files).

Amazon S3: Uses a two-bucket system for robust file handling:

Upload Bucket: A temporary staging area for new file uploads.

Organized Bucket: The main storage where files are copied and automatically sorted into folders by file type using an S3 Event Notification that triggers a Lambda function.

Infrastructure as Code (IaC):

Terraform: Defines and deploys all the AWS resources required for the application.

AI Services:

Hugging Face Inference API: Provides access to the facebook/bart-large-cnn model for summarization and title generation.

## Setup and Installation
To deploy this project yourself, follow these steps.

### Prerequisites
An AWS Account

Terraform CLI installed

Git installed

A Hugging Face API Token

### 1. Clone the Repository
Bash

git clone https://github.com/stlb57/SmartDrive-v2.git
cd your-repo-name
### 2. Configure Secrets
Create a file named terraform.tfvars in the root directory and add your Hugging Face API token:

Terraform

# In terraform.tfvars
huggingface_api_token = "hf_*******************"
(Remember, this file should be listed in your .gitignore to keep it private.)

### 3. Deploy the Backend
Initialize Terraform and deploy all the AWS resources.

Bash

# Initialize Terraform providers
terraform init

# Plan the deployment
terraform plan

# Apply the changes to deploy to your AWS account
terraform apply
When the deployment is complete, Terraform will output the api_gateway_invoke_url. You will need this for the next step.

### 4. Configure the Frontend
Open the index.html file.

Find the API_BASE constant at the top of the <script> tag.

Replace the placeholder URL with the api_gateway_invoke_url you got from the Terraform output.

JavaScript

const API_BASE = "https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com"; // <-- Paste your URL here
Save the index.html file.

## Usage
After completing the setup, simply open the index.html file in your web browser. You can now upload files and right-click on them to use the application's features.

## Future Improvements
CI/CD Pipeline: Automate deployment using GitHub Actions.

Remote State: Move the Terraform state file to an S3 bucket for better security and collaboration.

User Authentication: Add user login and registration using Amazon Cognito.

Database Integration: Use DynamoDB to store file metadata, summaries, and user information.

## License
This project is licensed under the MIT License.
