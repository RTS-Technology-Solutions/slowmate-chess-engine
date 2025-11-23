#!/bin/bash
# SlowMate Bot Monitoring Script
# Quick commands for managing the cloud-deployed bot

ZONE="us-central1-a"
VM="slowmate-bot-vm"

case "$1" in
    status)
        echo "=== Bot Service Status ==="
        gcloud compute ssh $VM --zone=$ZONE --command="sudo systemctl status slowmate-bot --no-pager -l"
        ;;
    logs)
        LINES=${2:-50}
        echo "=== Last $LINES Log Lines ==="
        gcloud compute ssh $VM --zone=$ZONE --command="sudo journalctl -u slowmate-bot -n $LINES --no-pager"
        ;;
    tail)
        echo "=== Following Bot Logs (Ctrl+C to stop) ==="
        gcloud compute ssh $VM --zone=$ZONE --command="sudo journalctl -u slowmate-bot -f"
        ;;
    restart)
        echo "=== Restarting Bot Service ==="
        gcloud compute ssh $VM --zone=$ZONE --command="sudo systemctl restart slowmate-bot && sleep 5 && sudo systemctl status slowmate-bot --no-pager"
        ;;
    stop)
        echo "=== Stopping Bot Service ==="
        gcloud compute ssh $VM --zone=$ZONE --command="sudo systemctl stop slowmate-bot && sudo systemctl status slowmate-bot --no-pager"
        ;;
    start)
        echo "=== Starting Bot Service ==="
        gcloud compute ssh $VM --zone=$ZONE --command="sudo systemctl start slowmate-bot && sleep 5 && sudo systemctl status slowmate-bot --no-pager"
        ;;
    vm-status)
        echo "=== VM Instance Status ==="
        gcloud compute instances describe $VM --zone=$ZONE --format="table(name,status,networkInterfaces[0].accessConfigs[0].natIP)"
        ;;
    ssh)
        echo "=== SSH into VM ==="
        gcloud compute ssh $VM --zone=$ZONE
        ;;
    games)
        LINES=${2:-20}
        echo "=== Recent Game Activity (last $LINES lines) ==="
        gcloud compute ssh $VM --zone=$ZONE --command="sudo journalctl -u slowmate-bot -n $LINES --no-pager | grep -E '(game|move|challenge|result|opponent)' | tail -30"
        ;;
    update-config)
        if [ -z "$2" ]; then
            echo "Usage: $0 update-config <local-config.yml>"
            exit 1
        fi
        echo "=== Uploading New Config ==="
        gcloud compute scp "$2" $VM:/tmp/config.yml --zone=$ZONE
        gcloud compute ssh $VM --zone=$ZONE --command="sudo cp /tmp/config.yml /opt/slowmate-bot/config.yml && sudo chown slowmate:slowmate /opt/slowmate-bot/config.yml && sudo chmod 600 /opt/slowmate-bot/config.yml"
        echo "Config updated. Restarting bot..."
        gcloud compute ssh $VM --zone=$ZONE --command="sudo systemctl restart slowmate-bot"
        ;;
    *)
        echo "SlowMate Bot Cloud Management"
        echo ""
        echo "Usage: $0 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  status          - Show bot service status"
        echo "  logs [N]        - Show last N log lines (default: 50)"
        echo "  tail            - Follow bot logs in real-time"
        echo "  games [N]       - Show recent game activity"
        echo "  restart         - Restart bot service"
        echo "  stop            - Stop bot service"
        echo "  start           - Start bot service"
        echo "  vm-status       - Show VM instance status"
        echo "  ssh             - SSH into the VM"
        echo "  update-config <file> - Upload new config.yml"
        echo ""
        echo "Examples:"
        echo "  $0 status                    # Check if bot is running"
        echo "  $0 logs 100                  # Show last 100 log lines"
        echo "  $0 tail                      # Watch logs in real-time"
        echo "  $0 games                     # See recent game activity"
        echo "  $0 update-config config.yml  # Upload new configuration"
        ;;
esac
