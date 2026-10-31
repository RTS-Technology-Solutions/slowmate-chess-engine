# SlowMate v3.5 - Deployment Checklist

## Local Prep
- [x] `lichess-bot/engines/SlowMate_v3.5/` package created from current root `src/`
- [x] `run_uci.py` launcher created in v3.5 package
- [x] trimmed opening book copied to `SlowMate_v3.5/data/openings/opening_book.json`
- [x] regression tests passed locally

## Cloud Deployment

### Pre-deployment
- [ ] Confirm VM access (`patss@34.56.74.200`)
- [ ] Confirm current bot service status

### Upload files
- [ ] `scp -r lichess-bot/engines/SlowMate_v3.5 patss@34.56.74.200:/tmp/`
- [ ] `scp lichess-bot/config.yml patss@34.56.74.200:/tmp/config_v3.5.yml`
- [ ] `scp lichess-bot/requirements.txt patss@34.56.74.200:/tmp/requirements_lichess_bot.txt`

### Install on VM
- [ ] backup `/opt/slowmate-bot/config.yml`
- [ ] install `/opt/slowmate-bot/engines/SlowMate_v3.5`
- [ ] copy `/tmp/config_v3.5.yml` to `/opt/slowmate-bot/config.yml`
- [ ] install deps: `python3 -m pip install --user -r /tmp/requirements_lichess_bot.txt`

### Verify and restart
- [ ] `echo "uci" | python3 /opt/slowmate-bot/engines/SlowMate_v3.5/run_uci.py`
- [ ] verify `id name SlowMate v3.5`
- [ ] restart `slowmate-bot.service`
- [ ] monitor logs for startup/game activity

### Post-deploy checks
- [ ] bot online on Lichess
- [ ] first game starts without errors
- [ ] telemetry strings visible in logs

## Rollback
- [ ] restore predeploy config backup
- [ ] restart service
