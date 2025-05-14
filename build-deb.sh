#!/bin/bash

# Script to build the Debian package for cloudzack-cli manually

set -e

echo "Building Debian package for cloudzack-cli..."

# Package information
PKG_NAME="cloudzack-cli"
PKG_VERSION="0.2.0"
PKG_ARCH="all"
MAINTAINER="Zack Langford <zack@cloudzack.com>"
DEPENDS="python3, python3-pip, curl, unzip"

# Create package directories
BUILD_DIR="build"
DEBIAN_DIR="$BUILD_DIR/DEBIAN"
INSTALL_DIR="$BUILD_DIR/opt/cloudzack-cli"
BIN_DIR="$BUILD_DIR/usr/local/bin"

# Clean up previous build
rm -rf "$BUILD_DIR"

# Create directory structure
mkdir -p "$DEBIAN_DIR" "$INSTALL_DIR" "$BIN_DIR"

# Copy shared scripts
cp -r shared "$INSTALL_DIR/"

# Create control file
cat > "$DEBIAN_DIR/control" << EOF
Package: $PKG_NAME
Version: $PKG_VERSION
Architecture: $PKG_ARCH
Maintainer: $MAINTAINER
Depends: $DEPENDS
Description: Custom AWS CLI tools and workflows
 CloudZack CLI provides customized scripts and Python workflows
 to quickly interact with AWS services like EC2 instances.
EOF

# Create postinst script
cat > "$DEBIAN_DIR/postinst" << EOF
#!/bin/bash

set -e

# Install Python dependencies
pip3 install boto3 botocore

# Install AWS CLI v2 if not already installed
if ! command -v aws &> /dev/null; then
  echo "Installing AWS CLI..."
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
  unzip -q /tmp/awscliv2.zip -d /tmp
  /tmp/aws/install
  rm -rf /tmp/aws /tmp/awscliv2.zip
fi

# Make scripts executable
find /opt/cloudzack-cli -name "*.py" -exec chmod +x {} \;

# Create symlinks in /usr/local/bin
for script in /opt/cloudzack-cli/shared/*.py; do
  script_name=\$(basename "\$script" .py)
  ln -sf "\$script" "/usr/local/bin/cloudzack-\$script_name"
done

# Create configuration directory for each user
if [ -d /home ]; then
  for user_home in /home/*; do
    if [ -d "\$user_home" ]; then
      user=\$(basename "\$user_home")
      mkdir -p "\$user_home/.cloudzack-cli"
      chown -R "\$user:\$user" "\$user_home/.cloudzack-cli"
    fi
  done
fi

echo "CloudZack CLI has been installed successfully!"
echo "REMINDER: You will need to run 'aws configure' to set up your AWS credentials."
echo "You will need your AWS Access Key ID and Secret Access Key."

exit 0
EOF

# Make postinst executable
chmod +x "$DEBIAN_DIR/postinst"

# Create symlinks for the scripts
for script in shared/*.py; do
  script_name=$(basename "$script" .py)
  ln -sf "/opt/cloudzack-cli/$script" "$BIN_DIR/cloudzack-$script_name"
done

# Build the package
dpkg-deb --build "$BUILD_DIR" "${PKG_NAME}_${PKG_VERSION}_${PKG_ARCH}.deb"

echo "Package built successfully!"
echo "You can find the .deb file in the current directory: ${PKG_NAME}_${PKG_VERSION}_${PKG_ARCH}.deb"
echo "To install it, run: sudo dpkg -i ${PKG_NAME}_${PKG_VERSION}_${PKG_ARCH}.deb"