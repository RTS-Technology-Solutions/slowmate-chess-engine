# SlowMate v3.3 - Deployment Checklist

## ✅ Local Preparation (COMPLETE)
- [x] Created `lichess-bot/engines/SlowMate_v3.3/` directory
- [x] Copied all v3.3 engine core files (engine.py, core/, search/, uci/, knowledge/)
- [x] Created `run_uci.py` launcher script
- [x] Fixed import paths (slowmate. → src.)
- [x] Updated `lichess-bot/config.yml` to point to v3.3
- [x] Updated greeting messages to v3.3
- [x] Tested UCI interface locally - **WORKING** ✓
- [x] Created deployment documentation

## 🚀 Cloud Deployment (TODO)

### Pre-Deployment
- [ ] Review CLOUD_DEPLOYMENT_V3_3.md
- [ ] Ensure SSH access to GCP VM (34.56.74.200)
- [ ] Verify current bot status on Lichess

### Upload Files
```bash
cd "s:/Programming/Chess Engines/SlowMate Chess Engine/slowmate-chess-engine/lichess-bot"
scp -r engines/SlowMate_v3.3 patss@34.56.74.200:/tmp/
scp config.yml patss@34.56.74.200:/tmp/config_v3.3.yml
```

### Install on VM
```bash
ssh patss@34.56.74.200
sudo mv /tmp/SlowMate_v3.3 /opt/slowmate-bot/engines/
sudo cp /opt/slowmate-bot/config.yml /opt/slowmate-bot/config.yml.v3.2.backup
sudo cp /tmp/config_v3.3.yml /opt/slowmate-bot/config.yml
sudo chown patss:patss /opt/slowmate-bot/config.yml
```

### Verify & Restart
```bash
cd /opt/slowmate-bot/engines/SlowMate_v3.3
echo "uci" | python3 run_uci.py  # Should show "SlowMate v3.3"
sudo systemctl restart slowmate-bot.service
sudo systemctl status slowmate-bot.service
sudo journalctl -u slowmate-bot.service -f
```

### Verify Online
- [ ] Check https://lichess.org/@/slowmate_bot is online
- [ ] Monitor first game for mate detection
- [ ] Confirm no errors in logs

## 📊 Post-Deployment Monitoring

### Immediate (First 5 games)
- [ ] Watch for mate-in-1 situations
- [ ] Verify no crashes or timeouts
- [ ] Check greeting shows "v3.3 - Mate Detection Fix"

### Short-term (After 20 games)
- [ ] Rating improvement: Target 1315-1365 (currently 1265)
- [ ] Win rate vs v7p3r_bot: Target 40-50% (currently 0%)
- [ ] Review losses for new patterns

### Long-term (After 50 games)
- [ ] Stable rating above 1300
- [ ] Positive record vs v7p3r_bot
- [ ] No mate-in-1 blunders detected

## 🔄 Rollback (if needed)
```bash
ssh patss@34.56.74.200
sudo cp /opt/slowmate-bot/config.yml.v3.2.backup /opt/slowmate-bot/config.yml
sudo systemctl restart slowmate-bot.service
```

## 📝 Notes
- Token file is in `.gitignore` - DO NOT commit
- lichess-bot directory is in `.gitignore` - maintained locally
- v3.3 fixes critical mate detection bug from v7p3r_bot game
- Expected improvement: +50-100 ELO
- Low risk: Targeted fix, easy rollback

---

**Current Status**: Ready for cloud deployment
**Next Step**: Run the upload commands and deploy to GCP VM
