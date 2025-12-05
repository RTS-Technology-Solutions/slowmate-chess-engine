# SlowMate v3.3 - Cloud Deployment Guide

## Status: READY FOR DEPLOYMENT

### What Changed
- **Version**: v3.2 → v3.3
- **Critical Fix**: Mate-in-1 detection in quiescence search
- **Files Updated**: 
  - `lichess-bot/engines/SlowMate_v3.3/` - Complete engine core (NEW)
  - `lichess-bot/config.yml` - Updated to point to v3.3

### Local Verification ✓
```bash
$ echo "uci" | python run_uci.py
id name SlowMate v3.3
id author SlowMate Team
uciok
```

## Deployment Steps

### 1. Connect to GCP VM
```bash
ssh patss@34.56.74.200
```

### 2. Upload v3.3 Engine
```bash
# From local machine (Windows bash)
cd "s:/Programming/Chess Engines/SlowMate Chess Engine/slowmate-chess-engine/lichess-bot"
scp -r engines/SlowMate_v3.3 patss@34.56.74.200:/tmp/
scp config.yml patss@34.56.74.200:/tmp/config_v3.3.yml
```

### 3. Install on VM
```bash
# SSH to VM
ssh patss@34.56.74.200

# Move engine to proper location
sudo mv /tmp/SlowMate_v3.3 /opt/slowmate-bot/engines/

# Backup current config
sudo cp /opt/slowmate-bot/config.yml /opt/slowmate-bot/config.yml.v3.2.backup

# Update config
sudo cp /tmp/config_v3.3.yml /opt/slowmate-bot/config.yml
sudo chown patss:patss /opt/slowmate-bot/config.yml
```

### 4. Verify Engine on VM
```bash
cd /opt/slowmate-bot/engines/SlowMate_v3.3
echo "uci" | python3 run_uci.py
# Should output: "id name SlowMate v3.3"
```

### 5. Restart Bot Service
```bash
# Check current status
sudo systemctl status slowmate-bot.service

# Restart with v3.3
sudo systemctl restart slowmate-bot.service

# Verify it started correctly
sudo systemctl status slowmate-bot.service

# Monitor logs
sudo journalctl -u slowmate-bot.service -f
```

### 6. Verify Live Connection
```bash
# Check bot is online at https://lichess.org/@/slowmate_bot
# Look for:
# - Bot shows as online
# - No error messages in journal logs
# - Ready to accept challenges
```

## Rollback Plan (if needed)

```bash
# SSH to VM
ssh patss@34.56.74.200

# Restore v3.2 config
sudo cp /opt/slowmate-bot/config.yml.v3.2.backup /opt/slowmate-bot/config.yml

# Restart service
sudo systemctl restart slowmate-bot.service
```

## Expected Improvements
- **Mate Detection**: No more mate-in-1 blunders like the v7p3r_bot game
- **Rating Gain**: +50 to +100 ELO expected
- **Win Rate**: 40-50% vs v7p3r_bot (from 0%)
- **Tactical**: Finds checkmates, avoids mate threats

## Post-Deployment Monitoring

### First 5 Games
- Watch for mate-in-1 situations
- Verify engine finds mates when available
- Check no regression in opening play

### After 20 Games
- Monitor rating improvement (target: 1315-1365)
- Track win rate vs v7p3r_bot
- Review any losses for new issues

## Config Changes Summary
```yaml
# OLD (v3.1):
engine:
  dir: "./engines/SlowMate_v3.1/"
  
greeting:
  hello: "Hi! I'm SlowMate v3.1. Good luck!"

# NEW (v3.3):
engine:
  dir: "./engines/SlowMate_v3.3/"
  
greeting:
  hello: "Hi! I'm SlowMate v3.3 - Mate Detection Fix. Good luck!"
```

## Technical Details
- Python interpreter: python3
- UCI Protocol: v2.2
- Hash: 64MB
- Time control: 60-600s base, 0-180s increment
- Game modes: casual, rated (bullet, blitz, rapid, classical)

---

**Ready to deploy!** All files are in place locally and tested. Follow the deployment steps above to update the cloud VM.
