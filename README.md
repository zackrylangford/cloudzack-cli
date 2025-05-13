# CloudZack CLI

A collection of customized scripts and Python workflows to quickly interact with AWS.

## Installation

### One-line installer (Ubuntu)

```bash
curl -sSL https://raw.githubusercontent.com/zackrylangford/cloudzack-cli/main/install.sh | sudo bash
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

## Available Commands

- `cloudzack-start-instance` - Start an AWS EC2 instance
- `cloudzack-stop-instance` - Stop an AWS EC2 instance

## Configuration

After installation, you'll need to configure your AWS credentials if you haven't done so during installation:

```bash
aws configure
```

You'll need your AWS Access Key ID and Secret Access Key.