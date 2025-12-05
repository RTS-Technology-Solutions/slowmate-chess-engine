#!/bin/bash
# SlowMate v3.3 - GCP Deployment Script
# This script deploys the v3.3 engine to the lichess-bot on GCP

set -e  # Exit on error

echo "================================================"
echo "SlowMate v3.3 - GCP Deployment"
echo "================================================"
echo ""

# Configuration
GCP_USER="patss"
GCP_IP="34.56.74.200"
GCP_HOST="${GCP_USER}@${GCP_IP}"
BOT_DIR="/opt/slowmate-bot"
ENGINE_NAME="SlowMate_v3.3"
LOCAL_ENGINE_DIR="lichess-bot/engines/${ENGINE_NAME}"
LOCAL_CONFIG="lichess-bot/config.yml"

echo "Step 1: Pre-deployment checks..."
echo "-----------------------------------"

# Check if local engine exists
if [ ! -d "$LOCAL_ENGINE_DIR" ]; then
    echo "❌ ERROR: Engine directory not found: $LOCAL_ENGINE_DIR"
    exit 1
fi
echo "✓ Engine directory found: $LOCAL_ENGINE_DIR"

# Check if config exists
if [ ! -f "$LOCAL_CONFIG" ]; then
    echo "❌ ERROR: Config file not found: $LOCAL_CONFIG"
    exit 1
fi
echo "✓ Config file found: $LOCAL_CONFIG"

# Test SSH connection
echo ""
echo "Step 2: Testing SSH connection to GCP..."
echo "-----------------------------------"
if ! ssh -o ConnectTimeout=10 "$GCP_HOST" "echo '✓ SSH connection successful'"; then
    echo "❌ ERROR: Cannot connect to GCP VM at $GCP_IP"
    echo "   Please check your SSH keys and network connection."
    exit 1
fi

echo ""
echo "Step 3: Uploading engine to GCP..."
echo "-----------------------------------"
echo "Uploading ${ENGINE_NAME} to ${GCP_HOST}:/tmp/"
scp -r "$LOCAL_ENGINE_DIR" "${GCP_HOST}:/tmp/"
echo "✓ Engine uploaded"

echo ""
echo "Uploading config.yml to ${GCP_HOST}:/tmp/config_v3.3.yml"
scp "$LOCAL_CONFIG" "${GCP_HOST}:/tmp/config_v3.3.yml"
echo "✓ Config uploaded"

echo ""
echo "Step 4: Installing on GCP VM..."
echo "-----------------------------------"

ssh "$GCP_HOST" << 'ENDSSH'
set -e

echo "→ Checking bot directory..."
if [ ! -d "/opt/slowmate-bot" ]; then
    echo "❌ ERROR: Bot directory /opt/slowmate-bot does not exist!"
    exit 1
fi

echo "→ Backing up current config..."
sudo cp /opt/slowmate-bot/config.yml /opt/slowmate-bot/config.yml.backup.$(date +%Y%m%d_%H%M%S)

echo "→ Installing engine..."
sudo rm -rf /opt/slowmate-bot/engines/SlowMate_v3.3
sudo mv /tmp/SlowMate_v3.3 /opt/slowmate-bot/engines/
sudo chown -R patss:patss /opt/slowmate-bot/engines/SlowMate_v3.3

echo "→ Updating config..."
sudo cp /tmp/config_v3.3.yml /opt/slowmate-bot/config.yml
sudo chown patss:patss /opt/slowmate-bot/config.yml
rm /tmp/config_v3.3.yml

echo "→ Testing engine..."
cd /opt/slowmate-bot/engines/SlowMate_v3.3
if echo "uci" | python3 run_uci.py | grep -q "SlowMate v3.3"; then
    echo "✓ Engine test passed - SlowMate v3.3 responding"
else
    echo "⚠️  WARNING: Engine test failed or unexpected response"
    exit 1
fi

echo ""
echo "✓ Installation complete"
ENDSSH

echo ""
echo "Step 5: Restarting bot service..."
echo "-----------------------------------"

ssh "$GCP_HOST" << 'ENDSSH'
set -e

echo "→ Checking service status..."
sudo systemctl is-active --quiet slowmate-bot.service && echo "  Bot service is currently running" || echo "  Bot service is currently stopped"

echo "→ Restarting service..."
sudo systemctl restart slowmate-bot.service

echo "→ Waiting for service to start..."
sleep 3

echo "→ Checking new service status..."
if sudo systemctl is-active --quiet slowmate-bot.service; then
    echo "✓ Bot service is running"
    sudo systemctl status slowmate-bot.service --no-pager -l | head -20
else
    echo "❌ ERROR: Service failed to start!"
    echo "Last 20 lines of service log:"
    sudo journalctl -u slowmate-bot.service -n 20 --no-pager
    exit 1
fi
ENDSSH

echo ""
echo "================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "================================================"
echo ""
echo "Next Steps:"
echo "  1. Verify bot is online: https://lichess.org/@/slowmate_bot"
echo "  2. Monitor first game for mate detection"
echo "  3. Check logs: ssh $GCP_HOST 'sudo journalctl -u slowmate-bot.service -f'"
echo ""
echo "Rollback (if needed):"
echo "  ssh $GCP_HOST"
echo "  sudo cp /opt/slowmate-bot/config.yml.backup.* /opt/slowmate-bot/config.yml"
echo "  sudo systemctl restart slowmate-bot.service"
echo ""
