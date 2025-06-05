Openly Data Cleaning and Scoring Pipeline
Overview
This project provides a pipeline to process messy lead data collected from various sources like CSV files, Google Sheets, and internal databases. It normalizes data fields, removes duplicates, scores leads based on their relevance to the corn starch supply chain, and exports the clean data to a CSV file. Infrastructure is deployed using AWS services via Terraform
Features
•	Normalize messy and inconsistent input data.
•	Deduplicate company records.
•	Score leads based on:
o	Presence of corn-starch in tags.
o	Keywords such as maize powder, starch, binder, and thickener in descriptions or tags.
o	Products containing corn starch in their ingredients.
•	Export clean, scored leads to a CSV file.
•	Infrastructure using:
o	S3 bucket (raw data storage)
o	EC2 instance (data processing)
o	RDS PostgreSQL (cleaned data storage)
o	CloudWatch logs (monitoring)
•	Scheduled daily processing with a cron job on EC2.
Project Structure
Openly-data-pipeline/
├── this_script.py             # Python script for data cleaning and scoring
├── requirements.txt           # Python dependencies
├── input_data.json             # Sample messy input data
├── cleaned_leads.csv           # Example cleaned and scored output
├── README.md                   # Project documentation
├── .gitignore                  # Ignore unnecessary files
├── Terraform/ (optional) # Terraform files not included
│   └── main.tf                  # Main Terraform configuration not included
└── tests/                       # Python test files
    └── test_this_script.py
Installation and Setup
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/lead-data-pipeline.git
cd lead-data-pipeline
2. Create a Virtual Environment
python -m venv .venv
Activate the environment:
Windows:
.venv\Scripts\activate
3. Install Python Dependencies
pip install -r requirements.txt
Usage
1.	Add your raw input data to input_data.json.
2.	Run the cleaning script:
python this_script.py
3.	Output will be saved as cleaned_leads.csv.
Running Tests
 How to Run the Tests
Make sure you have installed pytest:
pip install pytest
Then run in the terminal:
pytest tests/
You should see all tests passing:
============================= test session starts ==============================
collected 3 items

tests/test_this_script.py ...                                             [100%]

============================== 3 passed in 0.25s ===============================
Infrastructure Deployment
Infrastructure is provisioned with Terraform.
1. Setup
cd terraform/
terraform init
terraform apply
This will create:
•	S3 Bucket for raw data
•	EC2 instance with a daily cron job
•	RDS PostgreSQL instance for cleaned leads
•	CloudWatch log group for logging
Daily Automated Workflow
•	EC2 pulls input_data.json from the S3 bucket.
•	Processes and scores the leads.
•	Exports cleaned leads.
•	(Optional) Insert cleaned data into RDS database.
•	Logs are stored in CloudWatch.
Requirements
•	Python 3.8+
•	AWS Account
•	Terraform CLI
•	VS Code (Recommended)
•	AWS CLI configured locally
Author
•	Thomas Ayonuwe GitHub
