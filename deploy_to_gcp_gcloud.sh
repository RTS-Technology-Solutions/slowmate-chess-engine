#!/bin/bash
# SlowMate v3.3 - GCP Deployment via gcloud CLI
# This script deploys the v3.3 engine using gcloud commands

set -e  # Exit on error

echo "================================================"
echo "SlowMate v3.3 - GCP Deployment (gcloud)"
echo "================================================"
echo ""

# Configuration
GCP_PROJECT="slowmate-lichess-bot"
GCP_INSTANCE="slowmate-bot"  # Update this with your instance name
GCP_ZONE="us-central1-a"     # Update this with your zone
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

echo ""
echo "Step 2: Checking gcloud authentication..."
echo "-----------------------------------"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo "⚠️  Not authenticated with gcloud"
    echo "Please run: gcloud auth login"
    echo ""
    read -p "Press Enter to run gcloud auth login now, or Ctrl+C to exit..."
    gcloud auth login
fi
echo "✓ gcloud authenticated"

echo ""
echo "Step 3: Setting GCP project..."
echo "-----------------------------------"
gcloud config set project "$GCP_PROJECT"

echo ""
echo "Step 4: Finding GCP instance..."
echo "-----------------------------------"
echo "Looking for instances in project: $GCP_PROJECT"
echo ""
echo "Available instances:"
gcloud compute instances list --format="table(name,zone,status,externalIP)"
echo ""
read -p "Enter instance name (or press Enter for '$GCP_INSTANCE'): " USER_INSTANCE
if [ ! -z "$USER_INSTANCE" ]; then
    GCP_INSTANCE="$USER_INSTANCE"
fi

read -p "Enter zone (or press Enter for '$GCP_ZONE'): " USER_ZONE
if [ ! -z "$USER_ZONE" ]; then
    GCP_ZONE="$USER_ZONE"
fi

echo "Using: $GCP_INSTANCE in $GCP_ZONE"

echo ""
echo "Step 5: Uploading engine to GCP..."
echo "-----------------------------------"
echo "Uploading ${ENGINE_NAME}..."
gcloud compute scp --recurse "$LOCAL_ENGINE_DIR" "${GCP_INSTANCE}:/tmp/" --zone="$GCP_ZONE" --project="$GCP_PROJECT"
echo "✓ Engine uploaded"

echo ""
echo "Uploading config.yml..."
gcloud compute scp "$LOCAL_CONFIG" "${GCP_INSTANCE}:/tmp/config_v3.3.yml" --zone="$GCP_ZONE" --project="$GCP_PROJECT"
echo "✓ Config uploaded"

echo ""
echo "Step 6: Installing on GCP VM..."
echo "-----------------------------------"

gcloud compute ssh "${GCP_INSTANCE}" --zone="$GCP_ZONE" --project="$GCP_PROJECT" --command="
set -e

echo '→ Checking bot directory...'
if [ ! -d '/opt/slowmate-bot' ]; then
    echo '❌ ERROR: Bot directory /opt/slowmate-bot does not exist!'
    exit 1
fi

echo '→ Backing up current config...'
sudo cp /opt/slowmate-bot/config.yml /opt/slowmate-bot/config.yml.backup.\$(date +%Y%m%d_%H%M%S)

echo '→ Installing engine...'
sudo rm -rf /opt/slowmate-bot/engines/SlowMate_v3.3
sudo mv /tmp/SlowMate_v3.3 /opt/slowmate-bot/engines/
sudo chown -R \$(whoami):\$(whoami) /opt/slowmate-bot/engines/SlowMate_v3.3

echo '→ Updating config...'
sudo cp /tmp/config_v3.3.yml /opt/slowmate-bot/config.yml
sudo chown \$(whoami):\$(whoami) /opt/slowmate-bot/config.yml
rm /tmp/config_v3.3.yml

echo '→ Testing engine...'
cd /opt/slowmate-bot/engines/SlowMate_v3.3
if echo 'uci' | python3 run_uci.py | grep -q 'SlowMate v3.3'; then
    echo '✓ Engine test passed - SlowMate v3.3 responding'
else
    echo '⚠️  WARNING: Engine test failed or unexpected response'
    exit 1
fi

echo ''
echo '✓ Installation complete'
"

echo ""
echo "Step 7: Restarting bot service..."
echo "-----------------------------------"

gcloud compute ssh "${GCP_INSTANCE}" --zone="$GCP_ZONE" --project="$GCP_PROJECT" --command="
set -e

echo '→ Checking service status...'
sudo systemctl is-active --quiet slowmate-bot.service && echo '  Bot service is currently running' || echo '  Bot service is currently stopped'

echo '→ Restarting service...'
sudo systemctl restart slowmate-bot.service

echo '→ Waiting for service to start...'
sleep 3

echo '→ Checking new service status...'
if sudo systemctl is-active --quiet slowmate-bot.service; then
    echo '✓ Bot service is running'
    sudo systemctl status slowmate-bot.service --no-pager -l | head -20
else
    echo '❌ ERROR: Service failed to start!'
    echo 'Last 20 lines of service log:'
    sudo journalctl -u slowmate-bot.service -n 20 --no-pager
    exit 1
fi
"

echo ""
echo "================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "================================================"
echo ""
echo "Next Steps:"
echo "  1. Verify bot is online: https://lichess.org/@/slowmate_bot"
echo "  2. Monitor first game for mate detection"
echo "  3. Check logs: gcloud compute ssh ${GCP_INSTANCE} --zone=${GCP_ZONE} --command='sudo journalctl -u slowmate-bot.service -f'"
echo ""
echo "Rollback (if needed):"
echo "  gcloud compute ssh ${GCP_INSTANCE} --zone=${GCP_ZONE} --command='sudo cp /opt/slowmate-bot/config.yml.backup.* /opt/slowmate-bot/config.yml && sudo systemctl restart slowmate-bot.service'"
echo ""
