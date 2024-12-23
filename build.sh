#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies
apt-get update || true
apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev || true

# Upgrade pip and install build tools
pip install --upgrade pip
pip install --upgrade setuptools wheel

# Install packages with special handling
export LDFLAGS="-L/usr/local/lib"
export CPPFLAGS="-I/usr/local/include"
pip install --no-cache-dir Pillow==9.5.0
pip install --no-cache-dir psycopg2-binary==2.9.6

# Install remaining requirements
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --noinput
