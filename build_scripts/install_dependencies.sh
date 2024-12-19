#!/bin/bash
set -e

echo "Installing system dependencies..."
apt-get update
apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-pkg-resources \
    git

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing base dependencies..."
pip install --no-cache-dir setuptools==69.0.2 wheel==0.42.0 pkg_resources==0.0.0

echo "Installing project dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Verifying installations..."
python -c "import pkg_resources; print('pkg_resources installed successfully')"
