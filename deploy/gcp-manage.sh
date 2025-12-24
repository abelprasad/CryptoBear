#!/bin/bash
# CryptoBear - Quick Management Script
# Usage: ./gcp-manage.sh [command]

set -e

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project)}"
ZONE="${GCP_ZONE:-us-central1-a}"
VM_NAME="${VM_NAME:-cryptobear-bot}"
REMOTE_DIR="/home/cryptobear"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() { echo -e "${GREEN}ℹ️  $1${NC}"; }
print_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# Check if VM exists
check_vm() {
    if ! gcloud compute instances describe "$VM_NAME" --zone="$ZONE" --project="$PROJECT_ID" &>/dev/null; then
        print_error "VM '$VM_NAME' not found!"
        exit 1
    fi
}

# Show usage
usage() {
    echo "CryptoBear Management Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  status      - Show VM and container status"
    echo "  logs        - View bot logs (follow)"
    echo "  logs-tail   - View last 100 log lines"
    echo "  start       - Start the bot"
    echo "  stop        - Stop the bot"
    echo "  restart     - Restart the bot"
    echo "  ssh         - SSH into the VM"
    echo "  stats       - Show resource usage"
    echo "  vm-start    - Start the VM (if stopped)"
    echo "  vm-stop     - Stop the VM"
    echo "  vm-delete   - Delete the VM (WARNING: permanent)"
    echo ""
}

# Command handlers
cmd_status() {
    print_info "Checking VM status..."
    gcloud compute instances describe "$VM_NAME" --zone="$ZONE" --format="table(name,status,machineType,networkInterfaces[0].accessConfigs[0].natIP)"

    print_info "Checking container status..."
    gcloud compute ssh "$VM_NAME" --zone="$ZONE" --command="docker ps -a --filter name=cryptobear"
}

cmd_logs() {
    print_info "Following bot logs (Ctrl+C to exit)..."
    gcloud compute ssh "$VM_NAME" --zone="$ZONE" --command="docker logs -f cryptobear-bot"
}

cmd_logs_tail() {
    print_info "Last 100 log lines..."
    gcloud compute ssh "$VM_NAME" --zone="$ZONE" --command="docker logs --tail 100 cryptobear-bot"
}

cmd_start() {
    print_info "Starting bot..."
    gcloud compute ssh "$VM_NAME" --zone="$ZONE" --command="cd $REMOTE_DIR && docker-compose up -d"
    print_info "Bot started!"
}

cmd_stop() {
    print_info "Stopping bot..."
    gcloud compute ssh "$VM_NAME" --zone="$ZONE" --command="cd $REMOTE_DIR && docker-compose down"
    print_info "Bot stopped!"
}

cmd_restart() {
    print_info "Restarting bot..."
    gcloud compute ssh "$VM_NAME" --zone="$ZONE" --command="cd $REMOTE_DIR && docker-compose restart"
    print_info "Bot restarted!"
}

cmd_ssh() {
    print_info "Opening SSH connection..."
    gcloud compute ssh "$VM_NAME" --zone="$ZONE"
}

cmd_stats() {
    print_info "Resource usage (Ctrl+C to exit)..."
    gcloud compute ssh "$VM_NAME" --zone="$ZONE" --command="docker stats cryptobear-bot"
}

cmd_vm_start() {
    print_info "Starting VM..."
    gcloud compute instances start "$VM_NAME" --zone="$ZONE"
    print_info "VM started! Wait ~30 seconds for boot."
}

cmd_vm_stop() {
    print_warn "This will stop the VM and the bot!"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Stopping VM..."
        gcloud compute instances stop "$VM_NAME" --zone="$ZONE"
        print_info "VM stopped!"
    else
        print_info "Cancelled."
    fi
}

cmd_vm_delete() {
    print_error "WARNING: This will permanently delete the VM!"
    print_warn "All data on the VM will be lost."
    read -p "Type 'DELETE' to confirm: " confirm
    if [ "$confirm" = "DELETE" ]; then
        print_info "Deleting VM..."
        gcloud compute instances delete "$VM_NAME" --zone="$ZONE" --quiet
        print_info "VM deleted!"
    else
        print_info "Cancelled."
    fi
}

# Main script
if [ $# -eq 0 ]; then
    usage
    exit 0
fi

COMMAND=$1

case $COMMAND in
    status)
        check_vm
        cmd_status
        ;;
    logs)
        check_vm
        cmd_logs
        ;;
    logs-tail)
        check_vm
        cmd_logs_tail
        ;;
    start)
        check_vm
        cmd_start
        ;;
    stop)
        check_vm
        cmd_stop
        ;;
    restart)
        check_vm
        cmd_restart
        ;;
    ssh)
        check_vm
        cmd_ssh
        ;;
    stats)
        check_vm
        cmd_stats
        ;;
    vm-start)
        cmd_vm_start
        ;;
    vm-stop)
        check_vm
        cmd_vm_stop
        ;;
    vm-delete)
        cmd_vm_delete
        ;;
    *)
        print_error "Unknown command: $COMMAND"
        usage
        exit 1
        ;;
esac
