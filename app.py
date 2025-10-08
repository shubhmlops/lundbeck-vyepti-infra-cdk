#!/usr/bin/env python3
import aws_cdk as cdk
from my_eb_app.my_eb_app_stack import MyEbAppStack

# Replace with your S3 bucket and zip key
S3_BUCKET = "democdkbucketlundbeck"
S3_KEY = "Dockerfile.zip"

app = cdk.App()
MyEbAppStack(app, "MyEbAppStack", s3_bucket=S3_BUCKET, s3_key=S3_KEY, env=cdk.Environment(region="us-east-1"))
app.synth()