# CryptoBear Cloud Deployment Checklist

Follow this checklist to ensure a smooth deployment.

## Pre-Deployment Checklist

### 1. Google Cloud Setup
- [ ] Created GCP account
- [ ] Created or selected a project
- [ ] Enabled billing on the project
- [ ] Noted your Project ID: `________________`

### 2. Local Setup
- [ ] Installed Google Cloud SDK (`gcloud`)
- [ ] Authenticated with GCP: `gcloud auth login`
- [ ] Set default project: `gcloud config set project YOUR_PROJECT_ID`
- [ ] Verified authentication: `gcloud config list`

### 3. API Credentials
- [ ] Have Alpaca API key and secret
- [ ] Have Telegram bot token
- [ ] Have Telegram chat ID
- [ ] Created `.env` file with all credentials
- [ ] Tested bot locally (optional but recommended)

### 4. Configuration Review
- [ ] Reviewed `config/settings.yaml`
- [ ] Confirmed `sandbox: true` for paper trading
- [ ] Adjusted grid settings if desired
- [ ] Adjusted risk settings if desired

## Deployment Checklist

### Step 1: Prepare Deployment Scripts
**Linux/Mac/Git Bash:**
- [ ] Opened terminal in project directory
- [ ] Changed to deploy directory: `cd deploy`
- [ ] Made scripts executable: `chmod +x *.sh`

**Windows PowerShell:**
- [ ] Opened PowerShell as Administrator
- [ ] Changed to deploy directory: `cd deploy`

### Step 2: Create VM
**Linux/Mac/Git Bash:**
- [ ] Run: `./gcp-create-vm.sh`
- [ ] Noted the VM name (default: cryptobear-bot)
- [ ] Noted the zone (default: us-central1-a)
- [ ] Waited 2-3 minutes for initialization

**Windows PowerShell:**
- [ ] Run: `.\gcp-create-vm.ps1`
- [ ] Noted the VM name (default: cryptobear-bot)
- [ ] Noted the zone (default: us-central1-a)
- [ ] Waited 2-3 minutes for initialization

### Step 3: Verify VM Creation
- [ ] VM appears in GCP Console: https://console.cloud.google.com/compute/instances
- [ ] VM status shows "RUNNING"
- [ ] Can SSH to VM (optional): `gcloud compute ssh cryptobear-bot --zone=us-central1-a`

### Step 4: Deploy Bot
**Linux/Mac/Git Bash:**
- [ ] Return to deploy directory
- [ ] Run: `./gcp-deploy.sh`
- [ ] Watched for "Deployment complete!" message
- [ ] No errors during upload
- [ ] No errors during container build

**Windows PowerShell:**
- [ ] Return to deploy directory
- [ ] Run: `.\gcp-deploy.ps1`
- [ ] Watched for "Deployment complete!" message
- [ ] No errors during upload
- [ ] No errors during container build

## Post-Deployment Verification

### Immediate Checks (First 5 Minutes)
- [ ] Received Telegram notification: "🚀 Grid bot starting..."
- [ ] Received Telegram notification: "Grid initialized!"
- [ ] No error messages in Telegram

### Container Verification
**Linux/Mac/Git Bash:**
- [ ] Run: `./gcp-manage.sh status`
- [ ] Container status shows "Up"
- [ ] Run: `./gcp-manage.sh logs-tail`
- [ ] Logs show successful initialization
- [ ] No error messages in logs

**Direct commands (all platforms):**
```bash
# Check container is running
gcloud compute ssh cryptobear-bot --zone=us-central1-a --command='docker ps'

# Expected: Container "cryptobear-bot" with status "Up"
```

### Bot Verification
- [ ] Check Alpaca dashboard for open orders
- [ ] Should see 5 buy orders placed
- [ ] Order prices match expected grid levels
- [ ] Order sizes match configured risk (default 2%)

### Monitoring Setup
- [ ] Telegram notifications working
- [ ] Can view logs remotely
- [ ] Can access GCP Console
- [ ] Set up billing alerts in GCP Console

## 24-Hour Monitoring Checklist

### After 24 Hours
- [ ] Bot still running (check Telegram activity)
- [ ] No unexpected restarts (check logs)
- [ ] Orders functioning correctly
- [ ] No API errors in logs
- [ ] VM costs as expected in GCP Console

### Weekly Checks
- [ ] Review trading activity via Telegram
- [ ] Check profit/loss
- [ ] Review logs for any warnings
- [ ] Verify VM uptime
- [ ] Check GCP billing

## Troubleshooting Checklist

If bot not starting:
- [ ] Checked container logs: `./gcp-manage.sh logs-tail`
- [ ] Verified .env file uploaded to VM
- [ ] Verified API credentials are correct
- [ ] Restarted container: `./gcp-manage.sh restart`

If no Telegram notifications:
- [ ] Verified Telegram token in .env
- [ ] Verified chat ID in .env
- [ ] Checked bot logs for Telegram errors
- [ ] Tested Telegram bot manually

If no orders placed:
- [ ] Checked Alpaca account has funds
- [ ] Verified Alpaca API keys are correct
- [ ] Confirmed market is open (crypto markets are 24/7)
- [ ] Checked logs for API errors

If high costs:
- [ ] Verified using e2-micro instance
- [ ] Checked for unexpected data transfer
- [ ] Reviewed GCP billing breakdown
- [ ] Consider stopping VM when not needed

## Maintenance Checklist

### Monthly Maintenance
- [ ] Review bot performance
- [ ] Check for Docker image updates
- [ ] Update system packages on VM
- [ ] Review and archive old logs
- [ ] Verify backups (if configured)

### Code Updates
When updating bot code:
- [ ] Tested changes locally first
- [ ] Run deployment script: `./gcp-deploy.sh`
- [ ] Verified bot restarted successfully
- [ ] Monitored for first hour after update
- [ ] Documented changes made

## Emergency Procedures

### Stop Trading Immediately
```bash
./gcp-manage.sh stop
# OR
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='cd /home/cryptobear && docker-compose down'
```

### Stop VM (Stop All Charges)
```bash
./gcp-manage.sh vm-stop
# OR
gcloud compute instances stop cryptobear-bot --zone=us-central1-a
```

### Delete Everything
```bash
./gcp-manage.sh vm-delete
# OR
gcloud compute instances delete cryptobear-bot --zone=us-central1-a
```

## Success Criteria

Your deployment is successful when ALL of these are true:

✅ VM is running in GCP Console
✅ Container status shows "Up"
✅ Received Telegram startup notifications
✅ Orders visible in Alpaca dashboard
✅ Logs show no errors
✅ Bot trades automatically when conditions met
✅ Profit notifications received (when applicable)
✅ Costs within expected range (~$7-10/month)

## Notes and Observations

**Deployment Date:** _______________

**VM Name:** _______________

**Zone:** _______________

**Project ID:** _______________

**Initial Balance:** _______________

**Grid Settings:**
- Spread: _______________
- Count: _______________
- Risk per trade: _______________

**Issues Encountered:**
_________________________________
_________________________________
_________________________________

**Resolution:**
_________________________________
_________________________________
_________________________________

---

🧸 **Congratulations on your cloud deployment!**

Keep this checklist for reference and future deployments.
