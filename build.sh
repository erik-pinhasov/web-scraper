#!/bin/bash

set -o errexit

# Prompt the user for a password
read -sp "Enter your password for installation: " PASSWORD
echo

# Upgrade pip
echo "$PASSWORD" | sudo -S pip3 install --upgrade pip

# Install Python dependencies
echo "$PASSWORD" | sudo -S pip3 install -r requirements.txt

# Install Playwright without switching to the root user
PLAYWRIGHT_BROWSERS_PATH=$(npm config get prefix)/lib/node_modules/playwright
npm install playwright
export PATH=$PLAYWRIGHT_BROWSERS_PATH:$PATH

# Install Playwright dependencies
playwright install
playwright install-deps
