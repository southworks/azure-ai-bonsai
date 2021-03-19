#!/bin/bash
# This scripts pushes an image to the ACR.
# example call: "./push.sh leaving_home"
set -eux

source .env

MODEL=$1

docker tag $IMAGE_PREFIX-$MODEL $REPOSITORY.azurecr.io/$IMAGE_PREFIX-$MODEL
docker push $REPOSITORY.azurecr.io/$IMAGE_PREFIX-$MODEL
docker rmi $REPOSITORY.azurecr.io/$IMAGE_PREFIX-$MODEL
