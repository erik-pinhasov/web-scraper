apt-get update
apt-get install -y npm
pip install --upgrade pip
pip install -r /opt/render/project/src/requirements.txt
npm install -g playwright
ls -l /opt/render/project/python
npx playwright install
