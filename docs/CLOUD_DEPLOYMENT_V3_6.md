# SlowMate v3.6 - Lichess Deployment Runbook

## Status

Package and local smoke test are ready. **This runbook has not been executed**;
the GCP VM and its Lichess configuration remain unchanged.

Target: `slowmate-bot-vm`, project `slowmate-lichess-bot`, zone
`us-central1-a`. The live VM was previously observed using
`SlowMate_v3.4`; its config should be changed only after the new package is
transferred and verified.

## Package contents

`lichess-bot/engines/SlowMate_v3.6/` contains the current engine source,
`run_uci.py`, and the existing opening-book data. Syzygy support is optional,
but the 3-4-5-piece tablebase corpus is not included in the package.

## Before deployment

1. Authenticate `gcloud` in the operator's terminal.
2. From a Python environment with the repository requirements installed,
   verify the staged UCI identity locally:

   ```powershell
   'uci', 'quit' | python lichess-bot\engines\SlowMate_v3.6\run_uci.py
   ```

3. Confirm no game is in progress and agree on a maintenance window.
4. Do not copy the repository's local bot config to the VM. Update only the
   remote engine path and greeting so its existing credentials and settings
   are preserved.

## Transfer the new package

From the repository root:

```powershell
gcloud compute scp --recurse "lichess-bot\engines\SlowMate_v3.6" slowmate-bot-vm:/tmp/ --zone=us-central1-a --project=slowmate-lichess-bot
```

## Install and switch

Connect to the VM, then install the new version alongside v3.4. Do not remove
or overwrite the existing engine directory.

```bash
gcloud compute ssh slowmate-bot-vm --zone=us-central1-a --project=slowmate-lichess-bot

sudo cp -a /tmp/SlowMate_v3.6 /opt/slowmate-bot/engines/SlowMate_v3.6
sudo chown -R patss:patss /opt/slowmate-bot/engines/SlowMate_v3.6
sudo cp /opt/slowmate-bot/config.yml "/opt/slowmate-bot/config.yml.pre-v3.6.$(date -u +%Y%m%dT%H%M%SZ)"
sudoedit /opt/slowmate-bot/config.yml
```

In the remote config, change only:

```yaml
engine:
  dir: "./engines/SlowMate_v3.6/"
  name: "run_uci.py"
  interpreter: "python3"

greeting:
  hello: "Hi! I'm SlowMate v3.6. Good luck!"
  hello_spectators: "Welcome! Watching SlowMate v3.6 in action!"
```

Verify the new package before restarting the bot:

```bash
cd /opt/slowmate-bot/engines/SlowMate_v3.6
printf 'uci\nquit\n' | python3 run_uci.py
```

Confirm the output includes `id name SlowMate v3.6` and `uciok`. Then, only
after approving the service interruption:

```bash
sudo systemctl restart slowmate-bot.service
sudo systemctl is-active slowmate-bot.service
sudo journalctl -u slowmate-bot.service -n 40 --no-pager
```

Confirm the service is active, logs show v3.6, and the bot reconnects to
Lichess before ending the maintenance window.

## Rollback

Restore the config backup made immediately before the switch, then restart the
service. Keep both engine directories intact:

```bash
backup=$(ls -1t /opt/slowmate-bot/config.yml.pre-v3.6.* 2>/dev/null | head -n 1)
test -n "$backup"
sudo cp "$backup" /opt/slowmate-bot/config.yml
sudo systemctl restart slowmate-bot.service
sudo systemctl is-active slowmate-bot.service
```
