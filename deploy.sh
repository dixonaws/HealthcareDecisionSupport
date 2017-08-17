#!/bin/bash

# create the Lambda deployment package -- just a zip file
zip HealthcareDecisionSupport-deployment.zip HealthcareDecisionSupport.py

# publish the code to Lambda (the function must already exist)
aws --profile dixonaws@amazon.com --region us-east-1 lambda update-function-code --function-name HealthcareDecisionSupport --zip-file fileb://HealthcareDecisionSupport-deployment.zip --publish
