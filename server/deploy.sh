#!/bin/bash

temp_role=$(aws sts assume-role \
  --role-arn arn:aws:iam::858316752957:role/server-dev-ZappaLambdaExecutionRole \
  --role-session-name "DeployZappa")

echo "Became role/server-dev-ZappaLambdaExecutionRole"

export AWS_ACCESS_KEY_ID=$(echo $temp_role | jq .Credentials.AccessKeyId | xargs)
export AWS_SECRET_ACCESS_KEY=$(echo $temp_role | jq .Credentials.SecretAccessKey | xargs)
export AWS_SESSION_TOKEN=$(echo $temp_role | jq .Credentials.SessionToken | xargs)

zappa deploy dev || echo "No deploy needed"
zappa update dev
