#!/bin/bash
# This scripts builds a simulator with the required model.
# example call: "./build.sh leaving_home"
set -eux

source .env

MODEL=$1

docker build --build-arg MODEL=$MODEL . -t $IMAGE_PREFIX-$MODEL
