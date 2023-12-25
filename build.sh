PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set working directory

# Install npm
apt-get update
apt-get install -y npm
# Upgrade pip
pip install --upgrade pip

# Install additional dependencies
pip install -r $PROJECT_DIR/requirements.txt

npm install -g playwright

npx playwright install
ls -l /opt/render/project/src/web_app/app.py
