#! /usr/bin/env bash

# Get the secrets from AWS, Make sure you have the Jq installed
#sudo apt-get install jq -y 

secret1=$(aws secretsmanager get-secret-value --secret-id dylanwoo/ansible/vaultkey | jq -r '.SecretString' | awk -F "\"" '{print $4}')
echo ${secret1}


ansible-vault decrypt vault/vault.yml --ask-vault-password 