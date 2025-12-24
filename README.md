# CryptoBear 🧸

Automated grid trading bot for cryptocurrency markets. Trades BTC/USD on Alpaca using a systematic grid strategy to profit from price volatility.

## Features

- **Grid Trading Strategy** - Places buy/sell orders at fixed intervals to capture price swings
- **Alpaca Integration** - Paper trading support for risk-free testing
- **Telegram Notifications** - Real-time alerts for all trading activity
- **24/7 Cloud Deployment** - Run continuously on Google Cloud Platform
- **Automatic Recovery** - Auto-restarts on failures
- **Comprehensive Logging** - Detailed logs for monitoring and debugging

## How Grid Trading Works

The bot creates a "grid" of buy and sell orders:
- Places BUY orders below current market price
- When a buy fills, places a SELL order above it
- Captures profit from each price oscillation
- Continuously repeats for steady returns

**Example:**
- Buy BTC at $86,565 → Sell at $87,435 = $870 profit per cycle

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Local Development](#local-development)
- [Cloud Deployment](#cloud-deployment)
- [Usage](#usage)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Cost](#cost)
- [Security](#security)
- [Project Structure](#project-structure)

## Prerequisites

### Required

1. **Python 3.11+**
2. **Alpaca Account** - Get API keys from [alpaca.markets](https://alpaca.markets)
3. **Telegram Bot** - Create via [@BotFather](https://t.me/BotFather)

### For Cloud Deployment

4. **Google Cloud Account** - [cloud.google.com](https://cloud.google.com)
5. **gcloud CLI** - [Install Guide](https://cloud.google.com/sdk/docs/install)

## Quick Start

### Local Setup (5 Minutes)

```bash
# Clone repository
git clone https://github.com/abelprasad/CryptoBear.git
cd CryptoBear

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API credentials

# Run the bot
python main.py
```

### Cloud Deployment (3 Commands)

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Create VM
cd deploy
./gcp-create-vm.sh  # On Windows: .\gcp-create-vm.ps1

# Deploy bot (after 2-3 minutes)
./gcp-deploy.sh     # On Windows: .\gcp-deploy.ps1
```

## Configuration

### 1. Environment Variables (.env)

Create a `.env` file in the project root:

```bash
# Alpaca API (get from alpaca.markets)
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_API_SECRET=your_alpaca_secret
ALPACA_SANDBOX=true

# Telegram (create via @BotFather)
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

**How to get Telegram credentials:**

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions to get your TOKEN
3. Message your bot, then visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Find your CHAT_ID in the JSON response

### 2. Trading Parameters (config/settings.yaml)

```yaml
exchange: alpaca
pair: BTCUSD
sandbox: true  # Use paper trading

grid:
  spread: 0.005  # 0.5% spacing between orders
  count: 10      # Total grid levels (5 buy + 5 sell)

risk:
  per_trade: 0.02  # Risk 2% of balance per order

logging:
  level: INFO  # DEBUG | INFO | WARNING
```

**Parameter Guide:**

- `spread`: Distance between grid levels (smaller = more trades, smaller profits)
- `count`: Total number of grid levels
- `per_trade`: Percentage of account to risk per order

## Local Development

### Install Dependencies

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Run Locally

```bash
# Start the bot
python main.py

# The bot will:
# 1. Send startup notification to Telegram
# 2. Initialize grid and place orders
# 3. Monitor continuously for fills
# 4. Place counter-orders automatically
```

### Test Scripts

```bash
# Check current orders
python check_orders.py

# View profits
python check_profits.py

# Check market price
python check_price.py

# View activity log
python show_activity.py
```

## Cloud Deployment

### Prerequisites

```bash
# Install Google Cloud SDK
# Visit: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Deploy to Google Cloud

**Linux/Mac/Git Bash:**

```bash
cd deploy

# Make scripts executable
chmod +x *.sh

# Create VM (one-time setup)
./gcp-create-vm.sh

# Wait 2-3 minutes for initialization

# Deploy bot
./gcp-deploy.sh
```

**Windows PowerShell:**

```powershell
cd deploy

# Create VM (one-time setup)
.\gcp-create-vm.ps1

# Wait 2-3 minutes for initialization

# Deploy bot
.\gcp-deploy.ps1
```

### Management Commands

**Linux/Mac:**
```bash
# View logs
./gcp-manage.sh logs

# Check status
./gcp-manage.sh status

# Restart bot
./gcp-manage.sh restart

# Stop bot
./gcp-manage.sh stop

# SSH to VM
./gcp-manage.sh ssh
```

**Direct Commands (all platforms):**
```bash
# View logs
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='sudo docker logs -f cryptobear-bot'

# Restart bot
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='cd ~/cryptobear && sudo docker compose restart'

# Stop VM
gcloud compute instances stop cryptobear-bot --zone=us-central1-a

# Start VM
gcloud compute instances start cryptobear-bot --zone=us-central1-a

# Delete VM (stop all charges)
gcloud compute instances delete cryptobear-bot --zone=us-central1-a
```

## Usage

### Starting the Bot

**Locally:**
```bash
python main.py
```

**Cloud:**
```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='cd ~/cryptobear && sudo docker compose up -d'
```

### Stopping the Bot

**Stop bot only:**
```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='cd ~/cryptobear && sudo docker compose down'
```

**Stop VM (saves money):**
```bash
gcloud compute instances stop cryptobear-bot --zone=us-central1-a
```

### Updating Bot Code

After making changes to your code:

```bash
# Commit changes
git add .
git commit -m "your changes"
git push

# Redeploy to cloud
cd deploy
./gcp-deploy.sh  # or .\gcp-deploy.ps1 on Windows
```

## Monitoring

### Telegram Notifications

The bot sends real-time notifications for:
- Startup/shutdown events
- Grid initialization
- Order fills (buy/sell)
- Profit cycles
- Errors and warnings

### Logs

**View logs locally:**
```bash
tail -f logs/grid_bot_*.log
```

**View logs on cloud:**
```bash
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='sudo docker logs -f cryptobear-bot'
```

**Search for errors:**
```bash
grep ERROR logs/grid_bot_*.log
```

### Alpaca Dashboard

Monitor your account at [app.alpaca.markets](https://app.alpaca.markets):
- View open orders
- Check account balance
- Review trade history
- Monitor positions

## Troubleshooting

### Bot Not Starting

**Check logs:**
```bash
# Local
python main.py

# Cloud
gcloud compute ssh cryptobear-bot --zone=us-central1-a \
  --command='sudo docker logs cryptobear-bot'
```

**Common issues:**
- Missing or invalid API credentials in `.env`
- Alpaca API keys incorrect
- Telegram token invalid
- No internet connection

### No Telegram Notifications

1. Verify `TELEGRAM_TOKEN` is correct
2. Verify `TELEGRAM_CHAT_ID` is correct
3. Message your bot directly to test
4. Check bot logs for Telegram errors

### No Orders Placed

1. Check Alpaca account has funds
2. Verify API keys are for correct environment (paper/live)
3. Check logs for API errors
4. Ensure market is open (crypto markets are 24/7)

### VM Won't Start

```bash
# Check VM status
gcloud compute instances describe cryptobear-bot --zone=us-central1-a

# Check for quota issues in GCP Console
# Visit: console.cloud.google.com/compute/quotas
```

### Docker Issues

```bash
# Rebuild container
gcloud compute ssh cryptobear-bot --zone=us-central1-a
cd ~/cryptobear
sudo docker compose down
sudo docker compose build
sudo docker compose up -d
```

## Cost

### Local Development
**Free** - No costs for running locally

### Cloud Deployment

**Free Tier (eligible accounts):**
- $0/month for 1 e2-micro instance in US regions
- First 90 days or within free tier limits

**Standard Pricing:**
- VM (e2-micro): ~$7/month
- Disk (10 GB): ~$0.40/month
- Network: ~$1-2/month
- **Total: ~$7-10/month**

**Cost Optimization:**
- Stop VM when not trading: `gcloud compute instances stop cryptobear-bot --zone=us-central1-a`
- Delete VM when done: `gcloud compute instances delete cryptobear-bot --zone=us-central1-a`
- Set up billing alerts in GCP Console

## Security

### Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use paper trading first** - Set `sandbox: true` in config
3. **Start with small positions** - Adjust `per_trade` in config
4. **Monitor regularly** - Check Telegram notifications
5. **Set stop losses** - Manually monitor your account
6. **Rotate API keys** - Change keys regularly

### API Key Safety

- Store API keys in `.env` file only
- Never share or commit credentials
- Use read-only keys when possible
- Enable IP whitelisting on Alpaca (if available)

### GCP Security

```bash
# Restrict SSH access to your IP
gcloud compute firewall-rules create allow-ssh-my-ip \
  --allow tcp:22 \
  --source-ranges YOUR_IP/32 \
  --target-tags cryptobear-bot
```

## Project Structure

```
CryptoBear/
├── bear/                       # Main bot package
│   ├── __init__.py            # Config loader
│   ├── alpaca_rest.py         # Alpaca API client
│   ├── telegram.py            # Telegram notifications
│   ├── grid.py                # Grid calculation logic
│   ├── logger.py              # Logging configuration
│   └── trader.py              # Main bot orchestration
│
├── config/
│   └── settings.yaml          # Trading configuration
│
├── deploy/                    # Cloud deployment scripts
│   ├── README.md              # Deployment guide
│   ├── QUICKSTART.md          # Quick start guide
│   ├── DEPLOYMENT_CHECKLIST.md # Step-by-step checklist
│   ├── gcp-create-vm.sh       # Create VM (Linux/Mac)
│   ├── gcp-create-vm.ps1      # Create VM (Windows)
│   ├── gcp-deploy.sh          # Deploy bot (Linux/Mac)
│   ├── gcp-deploy.ps1         # Deploy bot (Windows)
│   ├── gcp-manage.sh          # Management commands
│   └── startup-script.sh      # VM initialization
│
├── logs/                      # Runtime logs (auto-created)
│   └── grid_bot_YYYYMMDD.log
│
├── .env.example               # Environment template
├── .env                       # Your credentials (gitignored)
├── .gitignore                 # Git exclusions
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Container orchestration
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── DOCUMENTATION.md           # Complete code documentation
```

## Documentation

- **README.md** (this file) - Getting started and usage
- **DOCUMENTATION.md** - Complete code walkthrough
- **deploy/README.md** - Detailed cloud deployment guide
- **deploy/QUICKSTART.md** - 5-minute quick start
- **deploy/DEPLOYMENT_CHECKLIST.md** - Step-by-step deployment

## Strategy Details

### Grid Configuration

**Default Settings:**
- Spread: 0.5% per grid level
- Levels: 10 (5 buy + 5 sell)
- Position size: 2% of account per order

**Example Grid at $87,000 BTC:**
```
Buy Orders:              Sell Orders:
$86,565 (-0.5%)         $87,435 (+0.5%)
$86,130 (-1.0%)         $87,870 (+1.0%)
$85,695 (-1.5%)         $88,305 (+1.5%)
$85,260 (-2.0%)         $88,740 (+2.0%)
$84,825 (-2.5%)         $89,175 (+2.5%)
```

### Profit Calculation

**Example Trade Cycle:**
1. Buy 0.02 BTC at $86,565 = $1,731.30
2. Sell 0.02 BTC at $87,435 = $1,748.70
3. **Profit: $17.40 per cycle**

The bot can execute multiple cycles per day depending on price volatility.

## Risk Warning

**Important:** Cryptocurrency trading carries significant risk. This bot:
- Does NOT guarantee profits
- May incur losses during trending markets
- Works best in ranging/sideways markets
- Should be tested with paper trading first

**Recommendations:**
- Start with paper trading (sandbox mode)
- Use only risk capital you can afford to lose
- Monitor the bot regularly
- Understand grid trading before using
- Start with conservative settings

## Support

- **Issues:** [GitHub Issues](https://github.com/abelprasad/CryptoBear/issues)
- **Discussions:** [GitHub Discussions](https://github.com/abelprasad/CryptoBear/discussions)

## License

This project is provided as-is for educational purposes. Use at your own risk.

## Acknowledgments

- Trading on [Alpaca](https://alpaca.markets)
- Notifications via [Telegram](https://telegram.org)
- Hosted on [Google Cloud Platform](https://cloud.google.com)

---

**Happy Trading! 🧸📈**

Remember: Always test with paper trading first!
