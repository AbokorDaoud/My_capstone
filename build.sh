#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies
apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    python3-dev \
    build-essential

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run Django commands
python manage.py collectstatic --no-input
python manage.py migrate
