#!/bin/bash
#
# SlowMate Lichess Bot - GCP VM Startup Script
# This script runs when the VM starts up
#

set -e

# Update system packages
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install Python 3 and pip
echo "Installing Python and dependencies..."
apt-get install -y python3 python3-pip git

# Create slowmate user
echo "Creating slowmate user..."
useradd -m -s /bin/bash slowmate || true

# Create directory for the bot
echo "Creating bot directory..."
mkdir -p /opt/slowmate-bot
chown slowmate:slowmate /opt/slowmate-bot

# Clone or copy bot code (will be done separately via gcloud scp)
echo "Bot directory ready at /opt/slowmate-bot"

# Install Python dependencies
if [ -f /opt/slowmate-bot/requirements.txt ]; then
    echo "Installing Python requirements..."
    pip3 install -r /opt/slowmate-bot/requirements.txt
fi

# Create systemd service
cat > /etc/systemd/system/slowmate-bot.service <<'EOF'
[Unit]
Description=SlowMate Lichess Chess Bot
After=network.target

[Service]
Type=simple
User=slowmate
WorkingDirectory=/opt/slowmate-bot
ExecStart=/usr/bin/python3 lichess-bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable slowmate-bot

echo "Startup script completed successfully"
echo "Bot service configured but not started yet"
echo "Upload bot code to /opt/slowmate-bot and start service with: systemctl start slowmate-bot"
