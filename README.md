# CloudZack CLI

A collection of customized scripts and Python workflows to quickly interact with AWS.

## Quick Installation (Ubuntu/Debian)

```bash
curl -sSL https://raw.githubusercontent.com/zackrylangford/cloudzack-cli/main/install | sudo bash

```

## Installation Options

### Using Debian Package (Recommended for Ubuntu/Debian)

1. Download the latest .deb package from the [Releases page](https://github.com/zackrylangford/cloudzack-cli/releases)

2. Install the package:
   ```bash
   sudo dpkg -i cloudzack-cli_0.2.0_all.deb
   sudo apt-get install -f  # Install any missing dependencies
   ```

### Manual installation

1. Clone the repository:
   ```bash
   git clone https://github.com/zackrylangford/cloudzack-cli.git
   ```

2. Run the installer:
   ```bash
   cd cloudzack-cli
   sudo bash ubuntu/install.sh
   ```

## Building the Debian Package

If you want to build the Debian package yourself:

1. Clone the repository:
   ```bash
   git clone https://github.com/zackrylangford/cloudzack-cli.git
   cd cloudzack-cli
   ```

2. Run the build script:
   ```bash
   ./build-deb.sh
   ```

3. The .deb file will be created in the current directory.

## Available Commands

- `cloudzack-start-instance` - Start an AWS EC2 instance
- `cloudzack-stop-instance` - Stop an AWS EC2 instance

## Configuration

After installation, you'll need to configure your AWS credentials:

```bash
aws configure
```

You'll need your AWS Access Key ID and Secret Access Key.

## Uninstallation

### Quick Uninstallation

```bash
curl -sSL https://raw.githubusercontent.com/zackrylangford/cloudzack-cli/main/uninstall | bash
```

### Manual Uninstallation

To remove CloudZack CLI from your system:

```bash
sudo apt-get remove cloudzack-cli
```

This will remove the package but keep configuration files. To remove everything including configuration:

```bash
sudo apt-get purge cloudzack-cli
```