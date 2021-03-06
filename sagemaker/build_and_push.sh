#!/usr/bin/env bash
# to execute: call make build_and_push from root dir

# The name of our algorithm
algorithm_name=models/senator-nlp-vote-prediction-2
profile=jeremy_sagemaker


chmod +x src/train
chmod +x src/serve

account=$(aws sts get-caller-identity --profile "${profile}" --query Account --output text)

region=us-east-1

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${algorithm_name}:latest"

# If the repository doesn't exist in ECR, create it.

aws ecr describe-repositories --repository-names "${algorithm_name}" --profile "${profile}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${algorithm_name}" --profile "${profile}" > /dev/null
fi

# Get the login command from ECR and execute it directly
aws ecr get-login-password --region ${region} --profile ${profile} | docker login --username AWS --password-stdin ${fullname}


export AWS_ACCESS_KEY_ID=$(aws --profile "${profile}" configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws --profile "${profile}" configure get aws_secret_access_key)

# Build the docker image locally with the image name and then push it to ECR
# with the full name.

docker build  -t ${algorithm_name} . \
--build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
--build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
--no-cache

docker tag ${algorithm_name} ${fullname}

docker push ${fullname}
