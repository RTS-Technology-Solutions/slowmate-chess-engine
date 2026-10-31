# SlowMate v3.5 - Cloud Deployment Guide

## Status: READY FOR DEPLOYMENT

This runbook deploys the new v3.5 package from:
- `lichess-bot/engines/SlowMate_v3.5/`

It includes:
- v3.5 engine/search updates
- Syzygy runtime support (optional, probes only when local tables exist)
- deterministic opening selection
- opening-book telemetry

## What Changed vs v3.3

- Engine path: `SlowMate_v3.3` -> `SlowMate_v3.5`
- Bot runtime supports opening-book env override (`SLOWMATE_OPENING_BOOK_PATH`)
- Deployment now includes dependency sync using `lichess-bot/requirements.txt`

## 1) Connect to VM

```bash
ssh patss@34.56.74.200
```

## 2) Upload Engine + Config

```bash
cd "s:/Programming/Chess Engines/SlowMate Chess Engine/slowmate-chess-engine/lichess-bot"
scp -r engines/SlowMate_v3.5 patss@34.56.74.200:/tmp/
scp config.yml patss@34.56.74.200:/tmp/config_v3.5.yml
scp requirements.txt patss@34.56.74.200:/tmp/requirements_lichess_bot.txt
```

## 3) Install on VM

```bash
ssh patss@34.56.74.200

sudo cp /opt/slowmate-bot/config.yml /opt/slowmate-bot/config.yml.v3.5.predeploy.backup

sudo rm -rf /opt/slowmate-bot/engines/SlowMate_v3.5
sudo mv /tmp/SlowMate_v3.5 /opt/slowmate-bot/engines/
sudo chown -R patss:patss /opt/slowmate-bot/engines/SlowMate_v3.5

sudo cp /tmp/config_v3.5.yml /opt/slowmate-bot/config.yml
sudo chown patss:patss /opt/slowmate-bot/config.yml

# Sync bot deps (fixes missing backoff/rich/etc)
python3 -m pip install --user -r /tmp/requirements_lichess_bot.txt
```

## 4) Update config engine path

In `/opt/slowmate-bot/config.yml`, ensure:

```yaml
engine:
  dir: "./engines/SlowMate_v3.5/"
  name: "run_uci.py"
```

Optional greeting update:

```yaml
greeting:
  hello: "Hi! I'm SlowMate v3.5. Good luck!"
```

## 5) Verify engine directly on VM

```bash
cd /opt/slowmate-bot/engines/SlowMate_v3.5
echo "uci" | python3 run_uci.py
# Expect: id name SlowMate v3.5
```

## 6) Restart service

```bash
sudo systemctl restart slowmate-bot.service
sudo systemctl status slowmate-bot.service
sudo journalctl -u slowmate-bot.service -f
```

## 7) Verify online

- https://lichess.org/@/slowmate_bot is online
- no startup errors in `journalctl`
- games begin normally

## Rollback

```bash
sudo cp /opt/slowmate-bot/config.yml.v3.5.predeploy.backup /opt/slowmate-bot/config.yml
sudo systemctl restart slowmate-bot.service
```
