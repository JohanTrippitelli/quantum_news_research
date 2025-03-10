#!/bin/bash

echo "🚀 Setting up your Python scraping environment..."

# Update package list (Linux/macOS)
echo "🔄 Updating package list..."
sudo apt update -y 2>/dev/null || echo "Skipping package list update..."

# Install necessary Python packages
echo "📦 Installing required Python packages..."
pip install selenium pyyaml requests pandas IPython openpyxl

echo "✅ Setup complete! You can now run your scraper."
