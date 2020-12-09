#!/usr/bin/env bash

# The name of our algorithm
algorithm_name=models/senator-nlp-vote-prediction
profile=jeremy_sagemaker

region=us-east-1

export AWS_ACCESS_KEY_ID=$(aws --profile "${profile}" configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws --profile "${profile}" configure get aws_secret_access_key)

# Build the docker image locally with the image name and then push it to ECR
# with the full name.

docker build  -t ${algorithm_name} . \
--build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
--build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
#--no-cache
