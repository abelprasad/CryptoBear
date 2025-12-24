# CryptoBear - Deploy to GCP (PowerShell version for Windows)
# Usage: .\gcp-deploy.ps1

param(
    [string]$ProjectId = (gcloud config get-value project),
    [string]$Zone = "us-central1-a",
    [string]$VMName = "cryptobear-bot",
    [string]$RemoteDir = "/home/cryptobear"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================="
Write-Host "CryptoBear Deployment to GCP"
Write-Host "==========================================="
Write-Host "VM: $VMName"
Write-Host "Zone: $Zone"
Write-Host "==========================================="
Write-Host ""

# Check if VM exists
Write-Host "Checking VM status..."
$vmExists = gcloud compute instances describe $VMName --zone=$Zone --project=$ProjectId 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: VM '$VMName' not found!" -ForegroundColor Red
    Write-Host "Create it first with: gcloud compute instances create ..." -ForegroundColor Yellow
    exit 1
}

# Check if .env exists
if (-Not (Test-Path ".env")) {
    Write-Host "Error: .env file not found!" -ForegroundColor Red
    Write-Host "Create .env with your API keys first (see .env.example)" -ForegroundColor Yellow
    exit 1
}

Write-Host "Creating remote directory structure..." -ForegroundColor Green
gcloud compute ssh $VMName --zone=$Zone --command="mkdir -p $RemoteDir"

Write-Host ""
Write-Host "Uploading code to VM..." -ForegroundColor Green

# Upload directories
gcloud compute scp --recurse .\bear "${VMName}:${RemoteDir}/" --zone=$Zone
gcloud compute scp --recurse .\config "${VMName}:${RemoteDir}/" --zone=$Zone

# Upload files
gcloud compute scp .\main.py "${VMName}:${RemoteDir}/" --zone=$Zone
gcloud compute scp .\requirements.txt "${VMName}:${RemoteDir}/" --zone=$Zone
gcloud compute scp .\Dockerfile "${VMName}:${RemoteDir}/" --zone=$Zone
gcloud compute scp .\docker-compose.yml "${VMName}:${RemoteDir}/" --zone=$Zone
gcloud compute scp .\.env "${VMName}:${RemoteDir}/" --zone=$Zone

Write-Host ""
Write-Host "Building and starting container on VM..." -ForegroundColor Green

$deployCommand = @"
cd $RemoteDir && \
docker-compose down || true && \
docker-compose build && \
docker-compose up -d
"@

gcloud compute ssh $VMName --zone=$Zone --command=$deployCommand

Write-Host ""
Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  View logs:     gcloud compute ssh $VMName --zone=$Zone --command='docker logs -f cryptobear-bot'"
Write-Host "  Restart bot:   gcloud compute ssh $VMName --zone=$Zone --command='cd $RemoteDir && docker-compose restart'"
Write-Host "  Stop bot:      gcloud compute ssh $VMName --zone=$Zone --command='cd $RemoteDir && docker-compose down'"
Write-Host "  SSH to VM:     gcloud compute ssh $VMName --zone=$Zone"
Write-Host ""
Write-Host "Monitor via Telegram for bot notifications!" -ForegroundColor Yellow
