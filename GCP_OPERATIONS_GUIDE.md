# SlowMate v3.3 - GCP Operations Guide

## Current GCP Setup

**Project**: slowmate-lichess-bot  
**VM Instance**: 34.56.74.200  
**User**: patss  
**Bot Location**: `/opt/slowmate-bot/`  
**Service**: `slowmate-bot.service`  
**Lichess Account**: https://lichess.org/@/slowmate_bot

## Directory Structure on GCP VM

```
/opt/slowmate-bot/
├── lichess-bot.py          # Main bot script
├── config.yml              # Bot configuration (points to engine)
├── requirements.txt        # Python dependencies
├── lib/                    # Bot library files
├── engines/                # Chess engines
│   ├── SlowMate_v3.1/     # Previous version
│   ├── SlowMate_v3.2/     # Previous version
│   └── SlowMate_v3.3/     # NEW - Current version
│       ├── run_uci.py     # UCI launcher
│       └── src/           # Engine source
│           ├── engine.py
│           ├── core/
│           ├── search/
│           ├── uci/
│           └── knowledge/
└── game_records/           # PGN game logs
```

## Deployment Methods

### Method 1: Automated Script (RECOMMENDED)

```bash
cd "s:/Programming/Chess Engines/SlowMate Chess Engine/slowmate-chess-engine"
bash deploy_to_gcp.sh
```

This script will:
1. Check SSH connection
2. Upload engine files
3. Upload config
4. Install on VM
5. Test engine
6. Restart service
7. Verify deployment

### Method 2: Manual Deployment

#### A. Upload Files
```bash
cd "s:/Programming/Chess Engines/SlowMate Chess Engine/slowmate-chess-engine/lichess-bot"

# Upload engine
scp -r engines/SlowMate_v3.3 patss@34.56.74.200:/tmp/

# Upload config
scp config.yml patss@34.56.74.200:/tmp/config_v3.3.yml
```

#### B. Install on VM
```bash
ssh patss@34.56.74.200

# Backup current config
sudo cp /opt/slowmate-bot/config.yml /opt/slowmate-bot/config.yml.v3.2.backup

# Install engine
sudo mv /tmp/SlowMate_v3.3 /opt/slowmate-bot/engines/
sudo chown -R patss:patss /opt/slowmate-bot/engines/SlowMate_v3.3

# Update config
sudo cp /tmp/config_v3.3.yml /opt/slowmate-bot/config.yml
sudo chown patss:patss /opt/slowmate-bot/config.yml
```

#### C. Test Engine
```bash
cd /opt/slowmate-bot/engines/SlowMate_v3.3
echo "uci" | python3 run_uci.py
# Should output: "id name SlowMate v3.3"
```

#### D. Restart Service
```bash
sudo systemctl restart slowmate-bot.service
sudo systemctl status slowmate-bot.service
```

## Service Management Commands

### Check Service Status
```bash
ssh patss@34.56.74.200
sudo systemctl status slowmate-bot.service
```

### View Live Logs
```bash
ssh patss@34.56.74.200
sudo journalctl -u slowmate-bot.service -f
```

### View Recent Logs
```bash
ssh patss@34.56.74.200
sudo journalctl -u slowmate-bot.service -n 100 --no-pager
```

### Restart Service
```bash
ssh patss@34.56.74.200
sudo systemctl restart slowmate-bot.service
```

### Stop Service
```bash
ssh patss@34.56.74.200
sudo systemctl stop slowmate-bot.service
```

### Start Service
```bash
ssh patss@34.56.74.200
sudo systemctl start slowmate-bot.service
```

## Verification Steps

### 1. Check Bot is Online
Visit: https://lichess.org/@/slowmate_bot

Should show:
- ✓ Online status indicator
- ✓ Recent games
- ✓ Available for challenges

### 2. Check Service Logs
```bash
ssh patss@34.56.74.200
sudo journalctl -u slowmate-bot.service -n 50
```

Look for:
- ✓ "SlowMate v3.3" in engine identification
- ✓ "Handling challenges"
- ✓ No error messages

### 3. Test Engine Directly
```bash
ssh patss@34.56.74.200
cd /opt/slowmate-bot/engines/SlowMate_v3.3
python3 run_uci.py
# Type: uci
# Type: isready
# Type: quit
```

### 4. Monitor First Game
```bash
ssh patss@34.56.74.200
sudo journalctl -u slowmate-bot.service -f
```

Watch for:
- ✓ Game acceptance
- ✓ Move generation
- ✓ No timeouts or crashes
- ✓ Proper mate detection

## Configuration Details

### Current config.yml Settings
```yaml
engine:
  dir: "./engines/SlowMate_v3.3/"
  name: "run_uci.py"
  interpreter: "python"
  protocol: "uci"
  
  uci_options:
    Hash: 64
    
  draw_or_resign:
    resign_enabled: true
    resign_score: -1000
    resign_moves: 5
    
challenge:
  concurrency: 1
  accept_bot: true
  max_base: 600        # 10 minutes
  min_base: 60         # 1 minute
  variants: [standard]
  time_controls: [bullet, blitz, rapid, classical]
  modes: [casual, rated]
```

## Troubleshooting

### Bot Shows Offline
```bash
ssh patss@34.56.74.200
sudo systemctl status slowmate-bot.service
sudo journalctl -u slowmate-bot.service -n 50
```

Common issues:
- Service not running → `sudo systemctl start slowmate-bot.service`
- Token expired → Update `config.yml` with new token
- Network issues → Check GCP firewall rules

### Engine Crashes
```bash
ssh patss@34.56.74.200
cd /opt/slowmate-bot/engines/SlowMate_v3.3
python3 run_uci.py  # Test manually
```

Check for:
- Python import errors
- Missing dependencies
- File permissions

### Service Won't Start
```bash
ssh patss@34.56.74.200
sudo journalctl -u slowmate-bot.service -n 100
```

Look for:
- Config file syntax errors
- Engine path incorrect
- Permission issues

## Rollback Procedures

### Rollback to v3.2
```bash
ssh patss@34.56.74.200

# Restore old config
sudo cp /opt/slowmate-bot/config.yml.v3.2.backup /opt/slowmate-bot/config.yml

# Restart service
sudo systemctl restart slowmate-bot.service

# Verify
sudo systemctl status slowmate-bot.service
```

### Rollback to v3.1
```bash
ssh patss@34.56.74.200

# Update config to point to v3.1
sudo sed -i 's|SlowMate_v3.3|SlowMate_v3.1|' /opt/slowmate-bot/config.yml

# Restart service
sudo systemctl restart slowmate-bot.service
```

## Monitoring & Performance

### Check Current Rating
Visit: https://lichess.org/@/slowmate_bot

### Download Recent Games
```bash
ssh patss@34.56.74.200
cd /opt/slowmate-bot/game_records
ls -lth | head -10
scp patss@34.56.74.200:/opt/slowmate-bot/game_records/*.pgn ./
```

### Watch Live Game
During a game, monitor logs:
```bash
ssh patss@34.56.74.200
sudo journalctl -u slowmate-bot.service -f
```

Look for:
- Move calculations
- Time management
- Position evaluations
- No mate-in-1 blunders!

## Expected v3.3 Improvements

### Performance Metrics
- **Current Rating**: 1265 ELO
- **Expected Rating**: 1315-1365 (+50-100)
- **vs v7p3r_bot**: 40-50% win rate (from 0%)

### Behavioral Changes
- ✓ Finds checkmates when available
- ✓ Avoids walking into mate-in-1
- ✓ Better check extension in search
- ✓ Checking moves prioritized

### What to Monitor
- First 5 games: No crashes, proper mate handling
- After 20 games: Rating improvement trend
- After 50 games: Stable performance above 1300

## Backup & Maintenance

### Create Full Backup
```bash
ssh patss@34.56.74.200
sudo tar -czf /tmp/slowmate-bot-backup-$(date +%Y%m%d).tar.gz /opt/slowmate-bot/
scp patss@34.56.74.200:/tmp/slowmate-bot-backup-*.tar.gz ./
```

### Update Python Dependencies
```bash
ssh patss@34.56.74.200
cd /opt/slowmate-bot
pip3 install -r requirements.txt --upgrade
sudo systemctl restart slowmate-bot.service
```

### Clean Old Logs
```bash
ssh patss@34.56.74.200
sudo journalctl --vacuum-time=7d
```

## Quick Reference Commands

```bash
# SSH to VM
ssh patss@34.56.74.200

# Check service
sudo systemctl status slowmate-bot.service

# Restart service
sudo systemctl restart slowmate-bot.service

# Live logs
sudo journalctl -u slowmate-bot.service -f

# Test engine
cd /opt/slowmate-bot/engines/SlowMate_v3.3 && echo "uci" | python3 run_uci.py

# Check bot online
curl https://lichess.org/@/slowmate_bot | grep -i online
```

---

**For automated deployment, run**: `bash deploy_to_gcp.sh`  
**For manual steps, follow**: Method 2 in this guide  
**For troubleshooting, see**: Troubleshooting section  
**For rollback, see**: Rollback Procedures section
