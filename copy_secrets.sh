#!/bin/bash

## Replace <REGION> with your AWS region code
REGION="us-east-1"

# Replace <SECRET_NAME> with the name of your secret
SECRET_NAME="AWS_ACCESS_KEYS"

# Replace <KEY> with the key whose value you want to retrieve from the secret
KEY="AWS_ACCESS_KEY"
SECRET_KEY="AWS_SECRET_ACCESS_KEY"
# Use the AWS CLI to retrieve the secret value
AWS_ACCESS_KEY=$(aws secretsmanager get-secret-value  --region $REGION --secret-id $SECRET_NAME --query 'SecretString' --output text | jq -r .$KEY)
AWS_SECRET_ACCESS_KEY=$(aws secretsmanager get-secret-value  --region $REGION --secret-id $SECRET_NAME --query 'SecretString' --output text | jq -r .$SECRET_KEY)
# Assign the secret value to an environment variable
export AWS_ACCESS_KEY=$AWS_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
# Verify that the environment variable has been set
gunicorn --config gunicorn-cfg.py run:app