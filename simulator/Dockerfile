# this is one of the cached base images available for ACI
FROM python:3.8.8

# Install libraries and dependencies
RUN apt-get update -qq && \
  apt-get install -yqq --no-install-recommends build-essential cmake zlib1g-dev swig > /dev/null && \
  apt-get clean && rm -r /var/lib/apt/lists/*

WORKDIR /src

# Copy and install simulator dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy simulator.
COPY src/*.py /src

ARG MODEL

# Copy model files.
COPY src/models/$MODEL /src/models/$MODEL

# Set environment variables.
ENV MODEL_NAME ${MODEL}
ENV SIM_PREFIX "Azure"

# This will be the command to run the simulator. Environment variables are provided by Bonsai so we don't need to read the local env file.
CMD python3 main.py --model "$MODEL_NAME" --use-env-file False
