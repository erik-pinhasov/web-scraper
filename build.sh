cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
# Upgrade pip
pip install --upgrade pip

# Install additional dependencies
pip install -r requirements.txt

npm install -g playwright

# Install Playwright dependencies
playwright install
