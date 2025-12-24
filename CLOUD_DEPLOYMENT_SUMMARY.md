# CryptoBear - Cloud Deployment Complete! 🧸☁️

Your trading bot is ready for 24/7 cloud deployment on Google Cloud Platform!

## What Has Been Set Up

### 1. Docker Containerization ✅
- **Dockerfile** - Production-ready container image
- **docker-compose.yml** - Local testing and VM deployment
- **.dockerignore** - Optimized build context

### 2. GCP Deployment Scripts ✅

**For Linux/Mac/Git Bash:**
- `deploy/gcp-create-vm.sh` - Create VM instance
- `deploy/gcp-deploy.sh` - Deploy/update bot code
- `deploy/gcp-manage.sh` - Manage bot (logs, restart, etc.)
- `deploy/startup-script.sh` - VM initialization

**For Windows PowerShell:**
- `deploy/gcp-create-vm.ps1` - Create VM instance
- `deploy/gcp-deploy.ps1` - Deploy/update bot code

### 3. Documentation ✅
- `deploy/README.md` - Complete deployment guide
- `deploy/QUICKSTART.md` - Quick start guide
- This summary file

## Getting Started (5 Minutes)

### Prerequisites
```bash
# 1. Install Google Cloud SDK
# Download from: https://cloud.google.com/sdk/docs/install

# 2. Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 3. Ensure your .env file exists with API credentials
# (Already done if you're running locally)
```

### Deploy to Cloud

**Option 1: Linux/Mac/Git Bash**
```bash
cd deploy

# Make scripts executable
chmod +x *.sh

# Create VM (one-time)
./gcp-create-vm.sh

# Wait 2 minutes, then deploy
./gcp-deploy.sh

# Check status
./gcp-manage.sh status

# View logs
./gcp-manage.sh logs
```

**Option 2: Windows PowerShell**
```powershell
cd deploy

# Create VM (one-time)
.\gcp-create-vm.ps1

# Wait 2 minutes, then deploy
.\gcp-deploy.ps1

# View logs
gcloud compute ssh cryptobear-bot --zone=us-central1-a --command='docker logs -f cryptobear-bot'
```

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         Google Cloud Platform           │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │   Compute Engine VM (e2-micro)    │ │
│  │                                   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │   Docker Container          │ │ │
│  │  │                             │ │ │
│  │  │   ┌──────────────────────┐  │ │ │
│  │  │   │  CryptoBear Bot      │  │ │ │
│  │  │   │  - Grid Trading      │  │ │ │
│  │  │   │  - Alpaca API        │  │ │ │
│  │  │   │  - Telegram Notify   │  │ │ │
│  │  │   └──────────────────────┘  │ │ │
│  │  │                             │ │ │
│  │  │   Logs: /app/logs           │ │ │
│  │  └─────────────────────────────┘ │ │
│  │                                   │ │
│  │   Auto-restart: ✅               │ │
│  │   24/7 Operation: ✅             │ │
│  └───────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
         │                  │
         │                  │
         ▼                  ▼
   Alpaca API         Telegram API
   (Trading)          (Notifications)
```

## Features

### Automatic Recovery ✅
- Container restarts on failure
- VM restarts on GCP maintenance
- Survives reboots

### Monitoring ✅
- Real-time Telegram notifications
- Docker logs accessible remotely
- GCP Console monitoring

### Security ✅
- Environment variables for secrets
- No credentials in code
- .env excluded from git

### Cost Optimization ✅
- Free tier eligible (e2-micro)
- ~$7-10/month standard pricing
- Can be stopped when not needed

## Quick Reference Commands

### Management Commands
```bash
# Linux/Mac/Git Bash
cd deploy
./gcp-manage.sh status      # Check VM and bot status
./gcp-manage.sh logs         # Follow logs (Ctrl+C to exit)
./gcp-manage.sh logs-tail    # Last 100 lines
./gcp-manage.sh restart      # Restart bot
./gcp-manage.sh stop         # Stop bot
./gcp-manage.sh start        # Start bot
./gcp-manage.sh ssh          # SSH into VM
./gcp-manage.sh stats        # Resource usage
./gcp-manage.sh vm-stop      # Stop VM (save costs)
./gcp-manage.sh vm-start     # Start VM
./gcp-manage.sh vm-delete    # Delete VM (WARNING)
```

### Direct Commands
```bash
# View logs
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker logs -f cryptobear-bot'

# Restart bot
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='cd /home/cryptobear && docker-compose restart'

# Check container status
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker ps'

# SSH into VM
gcloud compute ssh cryptobear-bot --zone=us-central1-a
```

## Cost Breakdown

**VM Instance (e2-micro):**
- vCPUs: 0.25-2 (burstable)
- RAM: 1 GB
- Cost: ~$7/month (or FREE with free tier)

**Boot Disk:**
- Size: 10 GB
- Type: Standard persistent disk
- Cost: ~$0.40/month

**Network:**
- Egress: Minimal (~1-2 GB/month)
- Cost: ~$1-2/month

**Total: ~$7-10/month** (or $0 if free tier eligible)

### Free Tier Eligibility
If your GCP account is eligible:
- 1 e2-micro instance in US regions (free)
- 30 GB standard persistent disk (free)
- 1 GB network egress (free)

Requirements:
- New GCP account (first 90 days)
- VM in US region (us-central1, us-east1, us-west1)
- Usage within limits

## Monitoring Your Bot

### 1. Telegram
You'll receive notifications for:
- Bot startup/shutdown
- Order fills
- Profit cycles
- Errors

### 2. Logs
```bash
# Real-time logs
./gcp-manage.sh logs

# Search for errors
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='docker logs cryptobear-bot 2>&1 | grep -i error'
```

### 3. GCP Console
- Visit: https://console.cloud.google.com/compute/instances
- Monitor: CPU, memory, disk, network
- View: VM status and health

## Updating Your Bot

After making code changes:

```bash
cd deploy
./gcp-deploy.sh
```

This will:
1. Upload new code
2. Rebuild container
3. Restart bot
4. Zero downtime deployment

## Stopping/Starting

### Pause Trading (Stop Bot)
```bash
./gcp-manage.sh stop
```
VM continues running, bot stops (saves API quota).

### Pause VM (Save Costs)
```bash
./gcp-manage.sh vm-stop
```
VM stops, charges stop (except disk storage).

### Resume
```bash
./gcp-manage.sh vm-start
# Wait ~30 seconds
./gcp-manage.sh start
```

## Troubleshooting

### Bot Not Starting
```bash
# Check logs for errors
./gcp-manage.sh logs-tail

# Check container status
./gcp-manage.sh status
```

Common issues:
- Missing .env file
- Invalid API credentials
- Insufficient funds in Alpaca account

### VM Not Accessible
```bash
# Check if VM is running
gcloud compute instances list

# Start if stopped
./gcp-manage.sh vm-start
```

### High Memory Usage
```bash
# Check resource usage
./gcp-manage.sh stats

# Upgrade VM if needed
gcloud compute instances set-machine-type cryptobear-bot \
  --machine-type e2-small --zone=us-central1-a
```

## Next Steps

1. **Deploy to cloud** following the commands above
2. **Monitor Telegram** for startup confirmation
3. **Check logs** to ensure bot is running correctly
4. **Set up billing alerts** in GCP Console
5. **Create VM snapshot** for backup (optional)

## Support Resources

- Full documentation: `deploy/README.md`
- Quick start guide: `deploy/QUICKSTART.md`
- GCP Documentation: https://cloud.google.com/docs
- GCP Console: https://console.cloud.google.com

## Security Reminders

- ✅ .env file is excluded from git
- ✅ Logs directory is excluded from git
- ✅ API credentials stored in environment variables
- ⚠️ Always use paper trading for testing
- ⚠️ Set up billing alerts to avoid surprises

## Files Created

```
CryptoBear/
├── Dockerfile                      # Container definition
├── docker-compose.yml              # Container orchestration
├── .dockerignore                   # Build optimization
├── deploy/
│   ├── README.md                   # Full documentation
│   ├── QUICKSTART.md              # Quick start guide
│   ├── gcp-create-vm.sh           # Create VM (Linux/Mac)
│   ├── gcp-create-vm.ps1          # Create VM (Windows)
│   ├── gcp-deploy.sh              # Deploy bot (Linux/Mac)
│   ├── gcp-deploy.ps1             # Deploy bot (Windows)
│   ├── gcp-manage.sh              # Management commands
│   └── startup-script.sh          # VM initialization
└── CLOUD_DEPLOYMENT_SUMMARY.md    # This file
```

---

🧸 **Your bot is ready for the cloud!**

Questions? Check `deploy/README.md` for detailed documentation.

Happy trading! 📈
