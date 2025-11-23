#!/bin/bash
# Quick deploy script
cd "s:/Programming/Chess Engines/SlowMate Chess Engine/slowmate-chess-engine/cloud-deployment"

gcloud compute instances create slowmate-bot-vm \
  --project=slowmate-lichess-bot \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=10GB \
  --metadata-from-file=startup-script=startup-script.sh \
  --tags=slowmate-bot
