#!/bin/bash

set -o errexit

# Extract the password from the environment variable
PASSWORD=$APP_PASSWORD

# Upgrade pip
pip3 install --upgrade pip

# Activate virtual environment (adjust the path accordingly)
source /path/to/your/venv/bin/activate

# Install Python dependencies within the virtual environment
pip3 install -r requirements.txt

# Install Playwright locally without switching to the root user
npm install playwright

# Set the PATH to include the locally installed Playwright binaries
PLAYWRIGHT_BROWSERS_PATH=$(npm bin)/playwright
export PATH=$PLAYWRIGHT_BROWSERS_PATH:$PATH

# Install Playwright dependencies
playwright install
playwright install-deps

# Deactivate the virtual environment
deactivate
