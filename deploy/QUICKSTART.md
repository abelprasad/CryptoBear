# CryptoBear Cloud Deployment - Quick Start

Deploy your trading bot to Google Cloud in under 5 minutes!

## Prerequisites

1. Google Cloud account with billing enabled
2. `gcloud` CLI installed and authenticated
3. `.env` file with your API credentials

## One-Time Setup

```bash
# 1. Authenticate with GCP
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Make scripts executable (Linux/Mac)
cd deploy
chmod +x *.sh

# 3. Create your .env file
cp .env.example .env
# Edit .env with your API keys
```

## Deploy to Cloud

### Step 1: Create VM
```bash
./gcp-create-vm.sh
```
Wait ~2 minutes for VM setup to complete.

### Step 2: Deploy Bot
```bash
./gcp-deploy.sh
```

That's it! Your bot is now running 24/7.

## Verify Deployment

Check Telegram - you should receive: "🚀 Grid bot starting..."

## Common Commands

```bash
# View live logs
./gcp-manage.sh logs

# Check status
./gcp-manage.sh status

# Restart bot
./gcp-manage.sh restart

# SSH into VM
./gcp-manage.sh ssh

# Stop bot (to save costs)
./gcp-manage.sh vm-stop
```

## Update Bot Code

After making changes:
```bash
./gcp-deploy.sh
```

## Windows Users

### Option 1: Use Git Bash or WSL
Install Git Bash or WSL (Windows Subsystem for Linux), then follow the Linux/Mac instructions above.

### Option 2: Use PowerShell
```powershell
# Create VM (one-time)
gcloud compute instances create cryptobear-bot `
  --zone=us-central1-a `
  --machine-type=e2-micro `
  --image-family=ubuntu-2204-lts `
  --image-project=ubuntu-os-cloud `
  --metadata-from-file=startup-script=startup-script.sh

# Deploy code
# (Upload files manually via GCP Console or use gcloud scp)
gcloud compute scp --recurse . cryptobear-bot:/home/cryptobear/ --zone=us-central1-a

# SSH and start bot
gcloud compute ssh cryptobear-bot --zone=us-central1-a
cd /home/cryptobear
docker-compose up -d
```

## Cost

**Free Tier:** $0/month (if eligible)
**Standard:** ~$7-10/month

Set up billing alerts in GCP Console!

## Troubleshooting

**Bot not starting?**
```bash
./gcp-manage.sh logs-tail
```

**Can't connect to VM?**
```bash
# Check VM is running
gcloud compute instances list

# Start if stopped
./gcp-manage.sh vm-start
```

**Need help?**
See full documentation in `deploy/README.md`

---

🧸 Happy Trading!
