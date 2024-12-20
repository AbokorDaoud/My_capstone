#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies for Pillow
apt-get update
apt-get install -y python3-dev python3-pip python3-setuptools libjpeg-dev zlib1g-dev

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --noinput
