cd "$(dirname "${BASH_SOURCE[0]}")" || exit

# Set Python path
export PYTHONPATH=./src

# Upgrade pip
pip install --upgrade pip

# Install additional dependencies
pip install -r requirements.txt

# Install Playwright
npm install -g playwright

# Install Playwright dependencies (specifying the platform explicitly)
PLAYWRIGHT_BROWSERS_PATH=./path/to/playwright/browsers/ npm install playwright
PLAYWRIGHT_BROWSERS_PATH=./path/to/playwright/browsers/ playwright install
PLAYWRIGHT_BROWSERS_PATH=./path/to/playwright/browsers/ playwright install-deps
