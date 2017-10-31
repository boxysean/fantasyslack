#!/bin/bash

zappa_role_file="assume-role-output.txt"

(aws sts assume-role \
  --role-arn arn:aws:iam::858316752957:role/server-dev-ZappaLambdaExecutionRole \
  --role-session-name "DeployZappa" > $zappa_role_file \
  && source $zappa_role_file && rm $zappa_role_file) || echo skipping assume role...

zappa update dev
