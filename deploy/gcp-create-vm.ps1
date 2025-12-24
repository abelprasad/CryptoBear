# CryptoBear - Create GCP VM (PowerShell version for Windows)
# Usage: .\gcp-create-vm.ps1

param(
    [string]$ProjectId = (gcloud config get-value project),
    [string]$Zone = "us-central1-a",
    [string]$VMName = "cryptobear-bot",
    [string]$MachineType = "e2-micro",
    [string]$BootDiskSize = "10GB"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================="
Write-Host "CryptoBear GCP Deployment"
Write-Host "==========================================="
Write-Host "Project: $ProjectId"
Write-Host "Zone: $Zone"
Write-Host "VM Name: $VMName"
Write-Host "Machine Type: $MachineType"
Write-Host "==========================================="
Write-Host ""

# Check if VM already exists
Write-Host "Checking if VM already exists..."
$vmExists = gcloud compute instances describe $VMName --zone=$Zone --project=$ProjectId 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Warning: VM '$VMName' already exists!" -ForegroundColor Yellow
    Write-Host "To delete it first, run: gcloud compute instances delete $VMName --zone=$Zone" -ForegroundColor Yellow
    exit 1
}

Write-Host "Creating VM instance..." -ForegroundColor Green

gcloud compute instances create $VMName `
    --project=$ProjectId `
    --zone=$Zone `
    --machine-type=$MachineType `
    --image-family=ubuntu-2204-lts `
    --image-project=ubuntu-os-cloud `
    --boot-disk-size=$BootDiskSize `
    --boot-disk-type=pd-standard `
    --tags=cryptobear-bot `
    --metadata-from-file=startup-script=.\startup-script.sh `
    --scopes=cloud-platform

Write-Host ""
Write-Host "VM created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Wait ~2 minutes for startup script to complete"
Write-Host "2. Deploy the bot: .\gcp-deploy.ps1"
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Cyan
Write-Host "  gcloud compute ssh $VMName --zone=$Zone --command='docker logs -f cryptobear-bot'"
Write-Host ""
