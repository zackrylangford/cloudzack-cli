#!/bin/bash

# cloudzack-cli installer for Ubuntu
# This script installs the cloudzack-cli tool and its dependencies

set -e

echo "Installing cloudzack-cli..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo"
  exit 1
fi

# Install dependencies
echo "Installing dependencies..."
apt-get update
apt-get install -y python3 python3-pip awscli

# Create installation directory
INSTALL_DIR="/opt/cloudzack-cli"
echo "Creating installation directory at $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Copy scripts
echo "Copying scripts..."
cp -r "$(dirname "$(dirname "$0")")/shared" "$INSTALL_DIR/"

# Make scripts executable
echo "Setting permissions..."
find "$INSTALL_DIR" -name "*.py" -exec chmod +x {} \;

# Create symlinks in /usr/local/bin
echo "Creating command links..."
for script in "$INSTALL_DIR"/shared/*.py; do
  script_name=$(basename "$script" .py)
  ln -sf "$script" "/usr/local/bin/cloudzack-$script_name"
done

# Create configuration directory
USER_HOME=$(eval echo ~${SUDO_USER})
CONFIG_DIR="$USER_HOME/.cloudzack-cli"
mkdir -p "$CONFIG_DIR"
chown -R ${SUDO_USER}:${SUDO_USER} "$CONFIG_DIR"

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install boto3 botocore

# Prompt for AWS configuration
echo "Do you want to configure AWS credentials now? (y/n)"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  # Run aws configure as the original user, not as root
  if [ -n "$SUDO_USER" ]; then
    su - $SUDO_USER -c "aws configure"
  else
    aws configure
  fi
else
  echo "REMINDER: You will need to run 'aws configure' to set up your AWS credentials before using cloudzack-cli."
  echo "You will need your AWS Access Key ID and Secret Access Key."
fi

echo "Installation complete!"
echo "You can now use cloudzack-cli commands like:"
echo "  cloudzack-start-instance"
echo "  cloudzack-stop-instance"