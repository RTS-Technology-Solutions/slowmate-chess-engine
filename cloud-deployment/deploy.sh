#!/bin/bash
#
# SlowMate Lichess Bot - Complete VM Deployment Script
# Run this script from your local machine to set up everything
#

set -e

PROJECT_ID="slowmate-lichess-bot"
INSTANCE_NAME="slowmate-bot-vm"
ZONE="us-central1-a"  # Change if needed
MACHINE_TYPE="e2-micro"  # Free tier eligible
IMAGE_FAMILY="ubuntu-2204-lts"
IMAGE_PROJECT="ubuntu-os-cloud"

echo "========================================="
echo "SlowMate Lichess Bot - GCP Deployment"
echo "========================================="
echo ""
echo "Project: $PROJECT_ID"
echo "Instance: $INSTANCE_NAME"
echo "Zone: $ZONE"
echo "Machine Type: $MACHINE_TYPE"
echo ""

# Set project
gcloud config set project $PROJECT_ID

# Create VM instance
echo "Creating VM instance..."
gcloud compute instances create $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --image-family=$IMAGE_FAMILY \
    --image-project=$IMAGE_PROJECT \
    --boot-disk-size=10GB \
    --boot-disk-type=pd-standard \
    --metadata-from-file=startup-script=startup-script.sh \
    --tags=slowmate-bot \
    --scopes=https://www.googleapis.com/auth/cloud-platform

echo ""
echo "Waiting for instance to start..."
sleep 30

# Wait for SSH to be ready
echo "Waiting for SSH to be ready..."
for i in {1..12}; do
    if gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="echo 'SSH ready'" 2>/dev/null; then
        echo "SSH is ready!"
        break
    fi
    echo "Attempt $i/12 - waiting 10 seconds..."
    sleep 10
done

# Upload bot code
echo ""
echo "Uploading bot code to VM..."
gcloud compute scp --recurse ../lichess-bot $INSTANCE_NAME:/tmp/ --zone=$ZONE

# Move bot code and set permissions
echo "Setting up bot on VM..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="
    sudo rm -rf /opt/slowmate-bot/*
    sudo cp -r /tmp/lichess-bot/* /opt/slowmate-bot/
    sudo chown -R slowmate:slowmate /opt/slowmate-bot
    sudo chmod 600 /opt/slowmate-bot/config.yml
    cd /opt/slowmate-bot && sudo pip3 install -r requirements.txt
"

# Start the bot service
echo ""
echo "Starting SlowMate bot service..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="
    sudo systemctl start slowmate-bot
    sudo systemctl status slowmate-bot --no-pager
"

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "Useful commands:"
echo "  View logs:    gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo journalctl -u slowmate-bot -f'"
echo "  Stop bot:     gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo systemctl stop slowmate-bot'"
echo "  Start bot:    gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo systemctl start slowmate-bot'"
echo "  SSH to VM:    gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo "  Delete VM:    gcloud compute instances delete $INSTANCE_NAME --zone=$ZONE"
echo ""
echo "Bot is now running at: https://lichess.org/@/slowmate_bot"
