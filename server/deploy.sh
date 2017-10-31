#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

temp_role=$(aws sts assume-role \
  --role-arn arn:aws:iam::858316752957:role/server-dev-ZappaLambdaExecutionRole \
  --role-session-name "DeployZappa")

echo "Became role/server-dev-ZappaLambdaExecutionRole"

export AWS_ACCESS_KEY_ID=$(echo $temp_role | jq .Credentials.AccessKeyId | xargs)
export AWS_SECRET_ACCESS_KEY=$(echo $temp_role | jq .Credentials.SecretAccessKey | xargs)
export AWS_SESSION_TOKEN=$(echo $temp_role | jq .Credentials.SessionToken | xargs)

# remove profile_name from zappa_settings.json

jq -a 'del(.dev.profile_name)' zappa_settings.json > zappa_settings.json.tmp

zappa deploy -s zappa_settings.json.tmp dev || echo "No deploy needed"
zappa update -s zappa_settings.json.tmp dev

rm zappa_settings.json.tmp
