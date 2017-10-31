#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

temp_role=$(aws sts assume-role \
  --role-arn arn:aws:iam::858316752957:role/FantasySlackDeployZappa \
  --role-session-name "FantasySlackDeployZappa")

echo "Became role/FantasySlackDeployZappa"

export AWS_ACCESS_KEY_ID=$(echo $temp_role | jq .Credentials.AccessKeyId | xargs)
export AWS_SECRET_ACCESS_KEY=$(echo $temp_role | jq .Credentials.SecretAccessKey | xargs)
export AWS_SESSION_TOKEN=$(echo $temp_role | jq .Credentials.SessionToken | xargs)

zappa deploy dev || echo "No deploy needed"
zappa update dev
