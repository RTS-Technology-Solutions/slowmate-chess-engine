# SlowMate Lichess Bot - Cloud Deployment Guide

## 🎉 Deployment Status: LIVE

**Bot is running!** 
- URL: https://lichess.org/@/slowmate_bot
- Status: Accepting challenges 24/7
- VM: `slowmate-bot-vm` @ `34.56.74.200`

## Overview

This directory contains scripts to deploy SlowMate v3.1 to Google Cloud Platform (GCP) for 24/7 operation.

## Prerequisites

1. **GCP Account** with billing enabled
2. **gcloud CLI** installed and authenticated
3. **Project Created**: `slowmate-lichess-bot`
4. **Compute Engine API** enabled

## Deployment Architecture

- **Instance Type**: e2-micro (free tier eligible)
- **OS**: Ubuntu 22.04 LTS
- **Region**: us-central1-a (configurable)
- **Auto-restart**: Yes (systemd service)
- **Disk**: 10GB standard persistent disk

## Quick Deploy

```bash
cd cloud-deployment
chmod +x deploy.sh
./deploy.sh
```

This will:
1. Create a new VM instance
2. Install Python and dependencies
3. Upload bot code
4. Configure systemd service
5. Start the bot

## Manual Deployment Steps

### 1. Create VM Instance

```bash
gcloud compute instances create slowmate-bot-vm \
    --project=slowmate-lichess-bot \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=10GB \
    --metadata-from-file=startup-script=startup-script.sh
```

### 2. Upload Bot Code

```bash
gcloud compute scp --recurse ../lichess-bot slowmate-bot-vm:/tmp/ --zone=us-central1-a
```

### 3. SSH and Configure

```bash
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a
```

Then on the VM:

```bash
sudo cp -r /tmp/lichess-bot /opt/slowmate-bot
sudo chown -R slowmate:slowmate /opt/slowmate-bot
cd /opt/slowmate-bot
sudo pip3 install -r requirements.txt
sudo systemctl start slowmate-bot
```

## Management Commands

### Quick Monitoring Script

Use the convenient monitoring script:

```bash
cd cloud-deployment
./monitor-bot.sh status       # Check if bot is running
./monitor-bot.sh logs 100     # View last 100 log lines
./monitor-bot.sh tail         # Follow logs in real-time
./monitor-bot.sh games        # See recent game activity
./monitor-bot.sh restart      # Restart the bot
```

### View Logs (Real-time)
```bash
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a \
    --command='sudo journalctl -u slowmate-bot -f'
```

### Check Bot Status
```bash
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a \
    --command='sudo systemctl status slowmate-bot'
```

### Restart Bot
```bash
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a \
    --command='sudo systemctl restart slowmate-bot'
```

### Stop Bot
```bash
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a \
    --command='sudo systemctl stop slowmate-bot'
```

### Update Bot Code
```bash
# Upload new code
gcloud compute scp --recurse ../lichess-bot slowmate-bot-vm:/tmp/ --zone=us-central1-a

# SSH and update
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a --command="
    sudo systemctl stop slowmate-bot
    sudo cp -r /tmp/lichess-bot/* /opt/slowmate-bot/
    sudo chown -R slowmate:slowmate /opt/slowmate-bot
    sudo systemctl start slowmate-bot
"
```

### Delete VM
```bash
gcloud compute instances delete slowmate-bot-vm --zone=us-central1-a
```

## Cost Estimates

- **e2-micro instance**: ~$7.50/month (or free tier if eligible)
- **10GB storage**: ~$0.40/month
- **Network egress**: Variable (minimal for chess bot)

**Total**: ~$8/month or FREE with GCP free tier

## Troubleshooting

### Bot Not Starting

Check logs:
```bash
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a \
    --command='sudo journalctl -u slowmate-bot -n 100'
```

### Dependencies Missing

```bash
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a
cd /opt/slowmate-bot
sudo pip3 install -r requirements.txt
sudo systemctl restart slowmate-bot
```

### Config Issues

Verify config file:
```bash
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a \
    --command='sudo cat /opt/slowmate-bot/config.yml'
```

## Security Notes

1. **API Token**: Stored in `config.yml` with restricted permissions (600)
2. **User Isolation**: Bot runs as dedicated `slowmate` user
3. **Firewall**: No inbound ports needed (bot connects outbound to Lichess)
4. **Automatic Updates**: System packages update on startup

## Monitoring

Check if bot is online at: https://lichess.org/@/slowmate_bot

View game records at: `/opt/slowmate-bot/game_records/`

## Backup Strategy

Game records are stored locally. To backup:

```bash
gcloud compute scp --recurse slowmate-bot-vm:/opt/slowmate-bot/game_records ./backup/ --zone=us-central1-a
```

## Future Enhancements

- [ ] Cloud logging integration
- [ ] Automated backups to Cloud Storage
- [ ] Health check monitoring
- [ ] Multi-region deployment
- [ ] Container-based deployment (Cloud Run)
