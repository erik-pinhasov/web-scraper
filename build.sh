apt-get update
apt-get install -y npm
pip install --upgrade pip
pip install -r /opt/render/project/src/requirements.txt
npm install -g playwright
npx playwright install

cd /opt/render/project/
ls -l
cd /opt/render/project/src
ls -l
cd /opt/render/project/src/src
ls -l
