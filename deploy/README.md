# CryptoBear Cloud Deployment Guide

Complete guide to deploying CryptoBear trading bot on Google Cloud Platform for 24/7 operation.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Detailed Setup](#detailed-setup)
4. [Managing the Bot](#managing-the-bot)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)
7. [Cost Optimization](#cost-optimization)

---

## Prerequisites

### 1. Google Cloud Account
- Create a GCP account at https://cloud.google.com
- Create a new project or use an existing one
- Enable billing (required for Compute Engine)

### 2. Install Google Cloud SDK
```bash
# Download from: https://cloud.google.com/sdk/docs/install
# Or use package manager:

# macOS
brew install google-cloud-sdk

# Ubuntu/Debian
sudo apt-get install google-cloud-sdk

# Windows
# Download installer from GCP website
```

### 3. Authenticate with GCP
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your API credentials:

```bash
cp .env.example .env
# Edit .env with your favorite editor
```

Required variables:
- `ALPACA_API_KEY` - Your Alpaca API key
- `ALPACA_API_SECRET` - Your Alpaca API secret
- `TELEGRAM_TOKEN` - Your Telegram bot token
- `TELEGRAM_CHAT_ID` - Your Telegram chat ID

---

## Quick Start

### Deploy in 3 Steps

```bash
# 1. Create the VM (one-time setup)
cd deploy
chmod +x *.sh
./gcp-create-vm.sh

# 2. Wait 2-3 minutes for VM initialization

# 3. Deploy the bot
./gcp-deploy.sh
```

That's it! Your bot is now running 24/7 in the cloud.

---

## Detailed Setup

### Step 1: Configure Deployment Settings

Set environment variables to customize your deployment:

```bash
# Optional: Customize VM configuration
export GCP_PROJECT_ID="your-project-id"     # Your GCP project
export GCP_ZONE="us-central1-a"             # VM location
export VM_NAME="cryptobear-bot"             # VM name
export MACHINE_TYPE="e2-micro"              # VM size (e2-micro is free tier)
```

### Step 2: Create the VM

```bash
cd deploy
./gcp-create-vm.sh
```

This script will:
- Create a new Compute Engine VM instance
- Install Docker and Docker Compose
- Set up the environment
- Configure auto-restart on failures

**VM Specs (default):**
- Machine Type: e2-micro (0.25-2 vCPU, 1 GB RAM)
- OS: Ubuntu 22.04 LTS
- Disk: 10 GB standard persistent disk
- Cost: ~$7-10/month (can be free tier eligible)

### Step 3: Verify VM Creation

```bash
# Check VM status
gcloud compute instances list

# SSH into VM (optional)
gcloud compute ssh cryptobear-bot --zone=us-central1-a
```

### Step 4: Deploy the Bot

```bash
./gcp-deploy.sh
```

This script will:
1. Build the Docker image locally
2. Upload code to the VM
3. Build the image on the VM
4. Start the bot container
5. Configure auto-restart

---

## Managing the Bot

### View Logs (Real-time)
```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker logs -f cryptobear-bot'
```

### Restart the Bot
```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='cd /home/cryptobear && docker-compose restart'
```

### Stop the Bot
```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='cd /home/cryptobear && docker-compose down'
```

### Start the Bot
```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='cd /home/cryptobear && docker-compose up -d'
```

### Update Bot Code
```bash
# After making changes locally
./gcp-deploy.sh
```

### Access VM Shell
```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a
```

### Delete the VM (stop all charges)
```bash
gcloud compute instances delete cryptobear-bot --zone=us-central1-a
```

---

## Monitoring

### 1. Telegram Notifications
The bot sends real-time notifications to Telegram:
- Bot startup/shutdown
- Order fills
- Profit cycles
- Errors and warnings

### 2. View Container Logs
```bash
# Last 100 lines
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker logs --tail 100 cryptobear-bot'

# Follow logs (Ctrl+C to exit)
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker logs -f cryptobear-bot'
```

### 3. Check Container Status
```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker ps -a'
```

### 4. View Bot Performance
```bash
# SSH into VM first
gcloud compute ssh cryptobear-bot --zone=us-central1-a

# Then run monitoring commands
cd /home/cryptobear

# View resource usage
docker stats cryptobear-bot

# View logs directory
ls -lh logs/
tail -f logs/grid_bot_*.log
```

### 5. GCP Console Monitoring
- Visit https://console.cloud.google.com/compute/instances
- Click on your VM to see:
  - CPU usage
  - Network traffic
  - Disk I/O
  - Serial port output

---

## Troubleshooting

### Bot Not Starting

**Check container status:**
```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a --command='docker ps -a'
```

**View error logs:**
```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker logs cryptobear-bot'
```

**Common issues:**
- Missing `.env` file → Upload it: `gcloud compute scp .env cryptobear-bot:/home/cryptobear/.env --zone=us-central1-a`
- Invalid API keys → Check your `.env` credentials
- Network issues → Check GCP firewall rules

### Container Keeps Restarting

```bash
# Check restart count
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker ps -a | grep cryptobear'

# View detailed logs
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker logs --tail 200 cryptobear-bot'
```

### High Memory Usage

```bash
# Check memory usage
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker stats --no-stream cryptobear-bot'

# If needed, upgrade VM
gcloud compute instances set-machine-type cryptobear-bot \
  --machine-type e2-small --zone=us-central1-a
# Then restart: gcloud compute instances start cryptobear-bot --zone=us-central1-a
```

### Cannot Connect to VM

```bash
# Check if VM is running
gcloud compute instances describe cryptobear-bot --zone=us-central1-a

# Start if stopped
gcloud compute instances start cryptobear-bot --zone=us-central1-a

# Check firewall rules
gcloud compute firewall-rules list
```

### Bot Not Trading

1. **Check Telegram** - Are you receiving notifications?
2. **Check market hours** - Is the market open?
3. **Check balance** - Does your Alpaca account have funds?
4. **Check logs** - Are there API errors?

```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker logs cryptobear-bot | grep -i error'
```

---

## Cost Optimization

### Current Setup (~$7-10/month)
- e2-micro instance: ~$7/month
- 10 GB standard disk: ~$0.40/month
- Network egress: ~$1-2/month

### Free Tier Eligible
If your GCP account is eligible for free tier:
- 1 e2-micro instance (US regions only)
- 30 GB standard persistent disk
- 1 GB network egress

**To use free tier:**
```bash
export MACHINE_TYPE="e2-micro"
export GCP_ZONE="us-central1-a"  # Must be US region
./gcp-create-vm.sh
```

### Further Optimization

**Use preemptible VM (up to 80% discount, but can be shut down):**
```bash
gcloud compute instances create cryptobear-bot \
  --preemptible \
  --machine-type=e2-micro \
  ...
```
⚠️ Not recommended for 24/7 trading bots!

**Use spot VM (similar to preemptible):**
```bash
gcloud compute instances create cryptobear-bot \
  --provisioning-model=SPOT \
  --machine-type=e2-micro \
  ...
```
⚠️ Not recommended for 24/7 trading bots!

**Monitor costs:**
- Visit https://console.cloud.google.com/billing
- Set up budget alerts
- Review cost breakdown

---

## Security Best Practices

### 1. Restrict SSH Access
```bash
# Only allow SSH from your IP
gcloud compute firewall-rules create allow-ssh-from-my-ip \
  --allow tcp:22 \
  --source-ranges YOUR_IP_ADDRESS/32 \
  --target-tags cryptobear-bot
```

### 2. Use Secret Manager (Advanced)
Instead of storing `.env` on the VM:

```bash
# Store secrets in GCP Secret Manager
gcloud secrets create alpaca-api-key --data-file=- <<< "your-key"
gcloud secrets create alpaca-api-secret --data-file=- <<< "your-secret"
```

Then modify the bot to read from Secret Manager.

### 3. Regular Updates
```bash
# Update system packages monthly
gcloud compute ssh cryptobear-bot --zone=us-central1-a --command='
  sudo apt-get update && sudo apt-get upgrade -y
'
```

### 4. Enable VM Auto-Restart
```bash
gcloud compute instances update cryptobear-bot \
  --zone=us-central1-a \
  --restart-on-failure
```

---

## Backup and Recovery

### Backup Logs
```bash
# Download logs to local machine
gcloud compute scp --recurse \
  cryptobear-bot:/home/cryptobear/logs \
  ./backup-logs \
  --zone=us-central1-a
```

### Create VM Snapshot
```bash
# Create snapshot of boot disk
gcloud compute disks snapshot cryptobear-bot \
  --zone=us-central1-a \
  --snapshot-names=cryptobear-backup-$(date +%Y%m%d)
```

### Restore from Snapshot
```bash
# Create new VM from snapshot
gcloud compute instances create cryptobear-bot-restored \
  --source-snapshot=cryptobear-backup-20251224 \
  --zone=us-central1-a
```

---

## Advanced Configuration

### Auto-Restart on Failure
The `docker-compose.yml` includes `restart: unless-stopped`, which means:
- Container restarts if it crashes
- Container restarts if VM reboots
- Container does NOT restart if you manually stop it

### Custom VM Configuration
Edit `gcp-create-vm.sh` to customize:
- Machine type (CPU/RAM)
- Disk size
- Region/zone
- Network settings

### Multiple Bots
To run multiple trading pairs:

```bash
# Create separate VMs
export VM_NAME="cryptobear-btc"
./gcp-create-vm.sh

export VM_NAME="cryptobear-eth"
./gcp-create-vm.sh
```

Or run multiple containers on one VM (modify docker-compose.yml).

---

## Support

If you encounter issues:

1. Check logs: `docker logs cryptobear-bot`
2. Check Telegram for error messages
3. Review this guide's troubleshooting section
4. Check GCP Console for VM health

---

## Next Steps

After deployment:

1. ✅ Monitor Telegram for startup notification
2. ✅ Verify orders are placed (check Alpaca dashboard)
3. ✅ Monitor logs for first 24 hours
4. ✅ Set up billing alerts in GCP Console
5. ✅ Document your configuration for future reference

Happy trading! 🧸📈
