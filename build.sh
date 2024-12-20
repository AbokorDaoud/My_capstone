#!/usr/bin/env bash
# exit on error
set -o errexit

# Install build dependencies
pip install --upgrade pip setuptools wheel

# Install packages that need compilation separately
pip install --no-binary :all: psycopg2-binary==2.9.9
pip install --no-binary :all: Pillow==10.1.0

# Install remaining requirements
grep -v "psycopg2-binary\|Pillow" requirements.txt | pip install -r /dev/stdin

python manage.py collectstatic --no-input
python manage.py migrate --noinput
