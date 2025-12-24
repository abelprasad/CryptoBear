#!/bin/bash
# CryptoBear VM Startup Script
# This script runs automatically when the VM boots
# It installs Docker and sets up the environment

set -e

echo "=========================================="
echo "CryptoBear VM Startup Script"
echo "=========================================="

# Update system
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install Docker
echo "Installing Docker..."
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker service
systemctl enable docker
systemctl start docker

# Install Docker Compose standalone (for compatibility)
DOCKER_COMPOSE_VERSION="2.24.5"
curl -SL "https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-linux-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create application directory
mkdir -p /home/cryptobear
cd /home/cryptobear

# Install git for easy code deployment
apt-get install -y git

echo ""
echo "✅ VM setup complete!"
echo "Docker version: $(docker --version)"
echo "Docker Compose version: $(docker-compose --version)"
echo ""
echo "Next: Clone your repository or copy your code to /home/cryptobear"
