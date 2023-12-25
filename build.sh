apt-get update
apt-get install -y npm
pip install --upgrade pip
pip install -r /opt/render/project/requirements.txt
npm install -g playwright
npx playwright install
