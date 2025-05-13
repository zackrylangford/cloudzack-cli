#!/bin/bash

# Script to build the Debian package for cloudzack-cli

set -e

echo "Building Debian package for cloudzack-cli..."

# Check for required packages
if ! command -v dpkg-buildpackage &> /dev/null; then
    echo "Installing build dependencies..."
    sudo apt-get update
    sudo apt-get install -y build-essential debhelper devscripts
fi

# Build the package
dpkg-buildpackage -us -uc -b

echo "Package built successfully!"
echo "You can find the .deb file in the parent directory."
echo "To install it, run: sudo dpkg -i ../cloudzack-cli_0.1.0_all.deb"