#!/bin/bash
# This scripts logs the user into the ACR.
set -eux

source .env

az acr login --name $REPOSITORY
