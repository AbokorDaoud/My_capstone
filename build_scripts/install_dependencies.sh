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
    git

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing wheel and setuptools..."
pip install --no-cache-dir wheel==0.42.0
pip install --no-cache-dir setuptools==69.0.2

echo "Installing project dependencies..."
pip install --no-cache-dir -r requirements.txt
