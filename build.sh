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
PATH_TO_FILE='/opt/render/project/src/web_app/app.py'

# Extract the directory names
IFS='/' read -ra DIRS <<< "$PATH_TO_FILE"

# Iterate through the directories
for dir in "${DIRS[@]}"; do
    # Print the current directory name
    echo "$dir"

    # Change to the current directory and perform ls
    ls "$dir"

    # If you want to list files recursively, uncomment the line below
    # ls -R "$dir"

    # Move into the current directory
    cd "$dir" || exit 1
done
