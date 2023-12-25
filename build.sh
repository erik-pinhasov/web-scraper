apt-get update
apt-get install -y npm
pip install --upgrade pip
pip install -r /opt/render/project/src/requirements.txt
npm install -g playwright
npx playwright install
cd /opt/render/project
ls -R

