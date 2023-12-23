set -o errexit

# Extract the password from the environment variable
PASSWORD=$APP_PASSWORD

# Upgrade pip
pip3 install --upgrade pip

# Install Python dependencies
pip3 install -r requirements.txt

# Install Playwright without switching to the root user
PLAYWRIGHT_BROWSERS_PATH=$(npm config get prefix)/lib/node_modules/playwright
npm install playwright
export PATH=$PLAYWRIGHT_BROWSERS_PATH:$PATH

# Install Playwright dependencies
playwright install
playwright install-deps
