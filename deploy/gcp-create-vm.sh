#!/bin/bash
# CryptoBear - Create GCP Compute Engine VM for 24/7 trading bot
# Usage: ./gcp-create-vm.sh

set -e

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project)}"
ZONE="${GCP_ZONE:-us-central1-a}"
VM_NAME="${VM_NAME:-cryptobear-bot}"
MACHINE_TYPE="${MACHINE_TYPE:-e2-micro}"  # Cost-effective for small bot
BOOT_DISK_SIZE="${BOOT_DISK_SIZE:-10GB}"

echo "==========================================="
echo "CryptoBear GCP Deployment"
echo "==========================================="
echo "Project: $PROJECT_ID"
echo "Zone: $ZONE"
echo "VM Name: $VM_NAME"
echo "Machine Type: $MACHINE_TYPE"
echo "==========================================="

# Check if VM already exists
if gcloud compute instances describe "$VM_NAME" --zone="$ZONE" --project="$PROJECT_ID" &>/dev/null; then
    echo "⚠️  VM '$VM_NAME' already exists!"
    echo "To delete it first, run: gcloud compute instances delete $VM_NAME --zone=$ZONE"
    exit 1
fi

echo "Creating VM instance..."

# Create VM with Container-Optimized OS
gcloud compute instances create "$VM_NAME" \
    --project="$PROJECT_ID" \
    --zone="$ZONE" \
    --machine-type="$MACHINE_TYPE" \
    --image-family="ubuntu-2204-lts" \
    --image-project="ubuntu-os-cloud" \
    --boot-disk-size="$BOOT_DISK_SIZE" \
    --boot-disk-type="pd-standard" \
    --tags="cryptobear-bot" \
    --metadata-from-file=startup-script=./startup-script.sh \
    --scopes=cloud-platform

echo ""
echo "✅ VM created successfully!"
echo ""
echo "Next steps:"
echo "1. Wait ~2 minutes for startup script to complete"
echo "2. SSH into the VM: gcloud compute ssh $VM_NAME --zone=$ZONE"
echo "3. Upload your .env file: gcloud compute scp .env $VM_NAME:~/cryptobear/.env --zone=$ZONE"
echo "4. Start the bot: ./deploy/gcp-deploy.sh"
echo ""
echo "To view logs:"
echo "  gcloud compute ssh $VM_NAME --zone=$ZONE --command='docker logs -f cryptobear-bot'"
