#!/bin/bash
# SlowMate v3.5 - GCP Deployment via gcloud CLI

set -e

echo "================================================"
echo "SlowMate v3.5 - GCP Deployment (gcloud)"
echo "================================================"
echo ""

GCP_PROJECT="slowmate-lichess-bot"
GCP_INSTANCE="slowmate-bot-vm"
GCP_ZONE="us-central1-a"
ENGINE_NAME="SlowMate_v3.5"
LOCAL_ENGINE_DIR="lichess-bot/engines/${ENGINE_NAME}"
LOCAL_CONFIG="lichess-bot/config.yml"
LOCAL_BOT_REQ="lichess-bot/requirements.txt"

echo "Step 1: Pre-deployment checks..."
if [ ! -d "$LOCAL_ENGINE_DIR" ]; then
  echo "ERROR: Missing engine directory: $LOCAL_ENGINE_DIR"
  exit 1
fi
if [ ! -f "$LOCAL_CONFIG" ]; then
  echo "ERROR: Missing config: $LOCAL_CONFIG"
  exit 1
fi
if [ ! -f "$LOCAL_BOT_REQ" ]; then
  echo "ERROR: Missing bot requirements: $LOCAL_BOT_REQ"
  exit 1
fi
echo "Prechecks OK"

echo "Step 2: gcloud auth/project"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
  echo "No active gcloud auth. Run: gcloud auth login"
  exit 1
fi
gcloud config set project "$GCP_PROJECT"

echo "Step 3: Upload artifacts"
gcloud compute scp --recurse "$LOCAL_ENGINE_DIR" "${GCP_INSTANCE}:/tmp/" --zone="$GCP_ZONE" --project="$GCP_PROJECT"
gcloud compute scp "$LOCAL_CONFIG" "${GCP_INSTANCE}:/tmp/config_v3.5.yml" --zone="$GCP_ZONE" --project="$GCP_PROJECT"
gcloud compute scp "$LOCAL_BOT_REQ" "${GCP_INSTANCE}:/tmp/requirements_lichess_bot.txt" --zone="$GCP_ZONE" --project="$GCP_PROJECT"

echo "Step 4: Install and verify on VM"
gcloud compute ssh "${GCP_INSTANCE}" --zone="$GCP_ZONE" --project="$GCP_PROJECT" --command="
set -e
sudo cp /opt/slowmate-bot/config.yml /opt/slowmate-bot/config.yml.backup.\$(date +%Y%m%d_%H%M%S)
sudo rm -rf /opt/slowmate-bot/engines/SlowMate_v3.5
sudo mv /tmp/SlowMate_v3.5 /opt/slowmate-bot/engines/
sudo chown -R \$(whoami):\$(whoami) /opt/slowmate-bot/engines/SlowMate_v3.5
sudo cp /tmp/config_v3.5.yml /opt/slowmate-bot/config.yml
sudo chown \$(whoami):\$(whoami) /opt/slowmate-bot/config.yml
python3 -m pip install --user -r /tmp/requirements_lichess_bot.txt
cd /opt/slowmate-bot/engines/SlowMate_v3.5
echo 'uci' | python3 run_uci.py | head -5
"

echo "Step 5: Restart service"
gcloud compute ssh "${GCP_INSTANCE}" --zone="$GCP_ZONE" --project="$GCP_PROJECT" --command="
set -e
sudo systemctl restart slowmate-bot.service
sleep 3
sudo systemctl status slowmate-bot.service --no-pager -l | head -20
"

echo "Deployment complete."
echo "Verify bot online: https://lichess.org/@/slowmate_bot"
echo "Follow logs: gcloud compute ssh ${GCP_INSTANCE} --zone=${GCP_ZONE} --project=${GCP_PROJECT} --command='sudo journalctl -u slowmate-bot.service -f'"
