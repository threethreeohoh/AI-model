#!/bin/bash

# Build the Docker image
docker build --platform linux/amd64 -t jwywoo/model_test .

# Push the Docker image to the repository
docker push jwywoo/model_test

