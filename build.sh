set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
playwright install
playwright install-deps
