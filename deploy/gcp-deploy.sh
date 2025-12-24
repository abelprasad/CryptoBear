#!/bin/bash
# CryptoBear - Deploy/Update bot on GCP VM
# Usage: ./gcp-deploy.sh

set -e

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project)}"
ZONE="${GCP_ZONE:-us-central1-a}"
VM_NAME="${VM_NAME:-cryptobear-bot}"
REMOTE_DIR="/home/cryptobear"

echo "==========================================="
echo "CryptoBear Deployment to GCP"
echo "==========================================="
echo "VM: $VM_NAME"
echo "Zone: $ZONE"
echo "==========================================="

# Check if VM exists
if ! gcloud compute instances describe "$VM_NAME" --zone="$ZONE" --project="$PROJECT_ID" &>/dev/null; then
    echo "❌ VM '$VM_NAME' not found!"
    echo "Create it first with: ./deploy/gcp-create-vm.sh"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Create .env with your API keys first (see .env.example)"
    exit 1
fi

echo "📦 Building Docker image locally..."
docker build -t cryptobear:latest .

echo ""
echo "📤 Uploading code to VM..."

# Create remote directory structure
gcloud compute ssh "$VM_NAME" --zone="$ZONE" --command="mkdir -p $REMOTE_DIR"

# Upload files
gcloud compute scp --recurse ./bear "$VM_NAME:$REMOTE_DIR/" --zone="$ZONE"
gcloud compute scp --recurse ./config "$VM_NAME:$REMOTE_DIR/" --zone="$ZONE"
gcloud compute scp ./main.py "$VM_NAME:$REMOTE_DIR/" --zone="$ZONE"
gcloud compute scp ./requirements.txt "$VM_NAME:$REMOTE_DIR/" --zone="$ZONE"
gcloud compute scp ./Dockerfile "$VM_NAME:$REMOTE_DIR/" --zone="$ZONE"
gcloud compute scp ./docker-compose.yml "$VM_NAME:$REMOTE_DIR/" --zone="$ZONE"
gcloud compute scp ./.env "$VM_NAME:$REMOTE_DIR/" --zone="$ZONE"

echo ""
echo "🐳 Building and starting container on VM..."

gcloud compute ssh "$VM_NAME" --zone="$ZONE" --command="
    cd $REMOTE_DIR && \
    docker-compose down || true && \
    docker-compose build && \
    docker-compose up -d
"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Useful commands:"
echo "  View logs:     gcloud compute ssh $VM_NAME --zone=$ZONE --command='docker logs -f cryptobear-bot'"
echo "  Restart bot:   gcloud compute ssh $VM_NAME --zone=$ZONE --command='cd $REMOTE_DIR && docker-compose restart'"
echo "  Stop bot:      gcloud compute ssh $VM_NAME --zone=$ZONE --command='cd $REMOTE_DIR && docker-compose down'"
echo "  SSH to VM:     gcloud compute ssh $VM_NAME --zone=$ZONE"
echo ""
echo "Monitor via Telegram for bot notifications! 🧸"
