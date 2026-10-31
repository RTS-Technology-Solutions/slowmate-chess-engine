# SlowMate v3.3 - Manual GCP Deployment Guide

## Quick Deploy Commands

**Instance**: slowmate-bot-vm  
**Zone**: us-central1-a  
**Project**: slowmate-lichess-bot

---

## Step-by-Step Deployment

### 1. Upload Engine Files
```bash
cd "s:/Programming/Chess Engines/SlowMate Chess Engine/slowmate-chess-engine/lichess-bot"

gcloud compute scp --recurse engines/SlowMate_v3.3 slowmate-bot-vm:/tmp/ \
  --zone=us-central1-a --project=slowmate-lichess-bot
```

### 2. Upload Config
```bash
gcloud compute scp config.yml slowmate-bot-vm:/tmp/config_v3.3.yml \
  --zone=us-central1-a --project=slowmate-lichess-bot
```

### 3. Install on VM
```bash
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a --project=slowmate-lichess-bot
```

Then run these commands on the VM:
```bash
# Backup current config
sudo cp /opt/slowmate-bot/config.yml /opt/slowmate-bot/config.yml.backup.$(date +%Y%m%d_%H%M%S)

# Install engine
sudo rm -rf /opt/slowmate-bot/engines/SlowMate_v3.3
sudo mv /tmp/SlowMate_v3.3 /opt/slowmate-bot/engines/
sudo chown -R $(whoami):$(whoami) /opt/slowmate-bot/engines/SlowMate_v3.3

# Update config
sudo cp /tmp/config_v3.3.yml /opt/slowmate-bot/config.yml
sudo chown $(whoami):$(whoami) /opt/slowmate-bot/config.yml

# Test engine
cd /opt/slowmate-bot/engines/SlowMate_v3.3
echo "uci" | python3 run_uci.py
# Should output: "id name SlowMate v3.3"

# Restart service
sudo systemctl restart slowmate-bot.service
sudo systemctl status slowmate-bot.service

# Monitor logs
sudo journalctl -u slowmate-bot.service -f
```

### 4. Verify Online
Visit: https://lichess.org/@/slowmate_bot

---

## One-Line Commands (copy-paste ready)

```bash
# Step 1: Upload engine
cd "s:/Programming/Chess Engines/SlowMate Chess Engine/slowmate-chess-engine/lichess-bot" && gcloud compute scp --recurse engines/SlowMate_v3.3 slowmate-bot-vm:/tmp/ --zone=us-central1-a --project=slowmate-lichess-bot

# Step 2: Upload config
gcloud compute scp config.yml slowmate-bot-vm:/tmp/config_v3.3.yml --zone=us-central1-a --project=slowmate-lichess-bot

# Step 3: SSH and install
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a --project=slowmate-lichess-bot --command="sudo cp /opt/slowmate-bot/config.yml /opt/slowmate-bot/config.yml.backup.\$(date +%Y%m%d_%H%M%S) && sudo rm -rf /opt/slowmate-bot/engines/SlowMate_v3.3 && sudo mv /tmp/SlowMate_v3.3 /opt/slowmate-bot/engines/ && sudo chown -R \$(whoami):\$(whoami) /opt/slowmate-bot/engines/SlowMate_v3.3 && sudo cp /tmp/config_v3.3.yml /opt/slowmate-bot/config.yml && sudo chown \$(whoami):\$(whoami) /opt/slowmate-bot/config.yml && cd /opt/slowmate-bot/engines/SlowMate_v3.3 && echo 'uci' | python3 run_uci.py | head -3"

# Step 4: Restart service
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a --project=slowmate-lichess-bot --command="sudo systemctl restart slowmate-bot.service && sleep 3 && sudo systemctl status slowmate-bot.service --no-pager | head -15"
```

---

## Rollback (if needed)
```bash
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a --project=slowmate-lichess-bot --command="sudo cp /opt/slowmate-bot/config.yml.backup.* /opt/slowmate-bot/config.yml && sudo systemctl restart slowmate-bot.service"
```
