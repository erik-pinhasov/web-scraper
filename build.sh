apt-get update
apt-get install -y npm
pip install --upgrade pip
cd /opt/render/project/src
pip install -r /opt/render/project/requirements.txt
npm install -g playwright
npx playwright install
cd /opt/render/project/src
export PYTHONPATH=/opt/render/project/src
