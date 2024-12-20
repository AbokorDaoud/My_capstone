#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip and install wheel first
pip install --upgrade pip
pip install wheel

# Install Pillow first
pip install --no-cache-dir Pillow==10.1.0

# Install remaining requirements
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --noinput
