PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $PROJECT_DIR
cd $PROJECT_DIR
ls -l
echo ----------------
# Set working directory
cd /opt/render/project/src
ls -l
# Install npm
apt-get update
apt-get install -y npm
# Upgrade pip
pip install --upgrade pip

# Install additional dependencies
pip install -r $PROJECT_DIR/requirements.txt

npm install -g playwright

npx playwright install

export PYTHONPATH=$PROJECT_DIR/src
ls -l
