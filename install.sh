#!/bin/bash

# cloudzack-cli one-line installer
# This script downloads the repository and runs the installation

set -e

echo "Downloading cloudzack-cli..."

# Install git if not already installed
if ! command -v git &> /dev/null; then
    echo "Installing git..."
    apt-get update
    apt-get install -y git
fi

# Create temporary directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Clone the repository
git clone https://github.com/zackrylangford/cloudzack-cli.git
cd cloudzack-cli

# Run the installer
bash ubuntu/install.sh

# Clean up
cd /
rm -rf "$TEMP_DIR"

echo "cloudzack-cli has been installed successfully!"