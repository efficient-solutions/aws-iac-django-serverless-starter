# Python version (use -bullseye variants on local arm64/Apple Silicon)
ARG VARIANT=3-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# Listens on this port at runtime
EXPOSE 8000

# Keep Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turn off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install additional OS packages
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#    && apt-get -y install --no-install-recommends <PACKAGE_NAME>

# Install Python requirements
COPY src/requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# Install the latest version of cfn-lint which is needed in the local environment only
# https://github.com/aws-cloudformation/cfn-lint-visual-studio-code
RUN pip3 install --disable-pip-version-check --no-cache-dir cfn-lint

# Install boto3 in the local environment
# RUN pip3 install --disable-pip-version-check --no-cache-dir "boto3==1.*"