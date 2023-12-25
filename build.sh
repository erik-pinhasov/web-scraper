PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Upgrade pip
pip install --upgrade pip

# Install additional dependencies
pip install -r $PROJECT_DIR/requirements.txt

# Install Playwright
npm install -g playwright

# Install Playwright dependencies
playwright install
playwright install-deps
