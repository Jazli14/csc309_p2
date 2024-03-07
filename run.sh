# Create virtual environment
python3 -m venv env

# Activate virtual environment
source env/bin/activate

# Install Python dependencies
pip install -r OneOnOne/requirements.txt

# Run Django migrations
python3 OneOnOne/manage.py migrate