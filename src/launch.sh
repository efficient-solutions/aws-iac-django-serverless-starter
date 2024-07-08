#!/bin/bash

# AWS Lambda wrapper script
# https://docs.aws.amazon.com/lambda/latest/dg/runtimes-modify.html#runtime-wrapper
#
# Uvicorn — ASGI web server implementation for Python
# https://www.uvicorn.org/

# Set environment variables, extend existing paths, and
# execute the command to start the Uvicorn server
PATH=$PATH:$LAMBDA_TASK_ROOT/bin \
PYTHONPATH=$PYTHONPATH:/opt/python:$LAMBDA_RUNTIME_DIR \
exec python -m uvicorn --port=$AWS_LWA_PORT --workers=1 project.asgi:application