apt-get update
apt-get install -y npm
pip install --upgrade pip
pip install -r /opt/render/project/src/requirements.txt
npm install -g playwright
npx playwright install
export PYTHONPATH=/opt/render/project/python/src/src/scrapers:/opt/render/project/python/src/src/web_app
