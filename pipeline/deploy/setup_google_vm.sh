#!/usr/bin/env bash
# ==============================================================================
# Setup Script for Agentic Books Distribution Engine on Google Cloud VM (Debian/Ubuntu)
# ==============================================================================
set -euo pipefail

echo "=================================================="
echo " Starting Google VM Setup for Agentic Books"
echo "=================================================="

# 1. Update system packages
sudo apt-get update -y
sudo apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    git \
    xvfb \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2

# 2. Setup Python virtual environment
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${PROJECT_DIR}"

if [ ! -d ".venv" ]; then
    echo "[INFO] Creating Python virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Install Playwright browser & system dependencies
echo "[INFO] Installing Playwright Chromium..."
playwright install chromium
playwright install-deps chromium

# 4. Create required directories
mkdir -p pipeline/growth pipeline/browser_profiles

echo "=================================================="
echo " Setup complete! Ready to run stealth daemon."
echo " To run daemon manually: "
echo "   source .venv/bin/activate"
echo "   python pipeline/stealth_browser/stealth_daemon.py --min-gap-minutes 5.0 --max-gap-minutes 20.0"
echo "=================================================="
