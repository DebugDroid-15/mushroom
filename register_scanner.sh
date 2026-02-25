#!/bin/bash
# Register sensor_scanner as a system command

echo "📦 Installing sensor_scanner command..."

# Copy to /usr/local/bin
sudo cp /home/mushroom/mushroom_project/sensor_scanner.py /usr/local/bin/sensor-scanner
sudo chmod +x /usr/local/bin/sensor-scanner

# Create wrapper script for easier use
sudo tee /usr/local/bin/scan-sensors > /dev/null << 'EOF'
#!/bin/bash
# Convenience wrapper for sensor scanner
python3 /home/mushroom/mushroom_project/sensor_scanner.py "$@"
EOF

sudo chmod +x /usr/local/bin/scan-sensors

echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  sensor-scanner [options]             # Run scanner once"
echo "  sensor-scanner --loop                # Continuous scanning" 
echo "  sensor-scanner --sensors 1 2        # Scan specific sensors"
echo "  scan-sensors --help                 # Show all options"
echo ""
echo "Quick test:"
scan-sensors
