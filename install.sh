#!/bin/bash
# Installation script for Soil Monitoring System
# Run on Raspberry Pi: bash install.sh

set -e

echo "🌱 Soil Monitoring System - Raspberry Pi Setup"
echo "==============================================="

# Check if running on Raspberry Pi
if ! uname -m | grep -q arm; then
    echo "⚠️  WARNING: Not running on ARM architecture"
fi

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip python3-venv git

# Create project directory
PROJECT_DIR="/home/pi/soil-monitor"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "📁 Creating project directory..."
    mkdir -p "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python packages
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create log directory
echo "📝 Creating log directory..."
sudo mkdir -p /var/log/soil-monitor
sudo chown pi:pi /var/log/soil-monitor
sudo chmod 755 /var/log/soil-monitor

# Install systemd service
echo "⚙️  Installing systemd service..."
sudo cp soil-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable soil-monitor

# Configure UART (requires reboot)
echo ""
echo "🔌 UART Configuration"
echo "====================="
echo "To enable UART on Raspberry Pi:"
echo "1. Run: sudo raspi-config"
echo "2. Go to Interface Options > Serial Port"
echo "3. Disable login shell on serial"
echo "4. Enable serial port hardware"
echo "5. Reboot"
echo ""

# Offer to test
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Configure Raspberry Pi UART (see above)"
echo "2. Wire RS-485 converter and sensors"
echo "3. Set correct Modbus IDs on sensors (1-4)"
echo "4. Run: sudo systemctl start soil-monitor"
echo "5. View logs: sudo journalctl -u soil-monitor -f"
echo ""
echo "Access dashboard: http://<raspberry_pi_ip>:5000"
echo ""

# Test Modbus (optional)
read -p "Test Modbus connection now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Testing Modbus connection..."
    python3 modbus_sensor.py
fi
