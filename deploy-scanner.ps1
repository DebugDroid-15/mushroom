# Deploy and register sensor scanner as system command

Write-Host "Deploying sensor_scanner..." -ForegroundColor Green

# Step 1: Upload sensor_scanner.py
scp -o StrictHostKeyChecking=no c:\Downloads\mushroom\sensor_scanner.py mushroom@raspberrypi.local:/home/mushroom/mushroom_project/sensor_scanner.py
if ($LASTEXITCODE -ne 0) { Write-Host "❌ Failed to upload sensor_scanner.py"; exit 1 }

# Step 2: Register as system command
Write-Host "Registering scanner command..." -ForegroundColor Green
ssh -o StrictHostKeyChecking=no mushroom@raspberrypi.local @"
sudo cp /home/mushroom/mushroom_project/sensor_scanner.py /usr/local/bin/sensor-scanner
sudo chmod +x /usr/local/bin/sensor-scanner

sudo tee /usr/local/bin/scan-sensors > /dev/null << 'EOF'
#!/bin/bash
python3 /home/mushroom/mushroom_project/sensor_scanner.py `$@
EOF

sudo chmod +x /usr/local/bin/scan-sensors
echo 'Sensor scanner registered!'
"@

Write-Host "`n✅ Sensor scanner is now registered!" -ForegroundColor Cyan
Write-Host "`nUsage commands on Pi:"  -ForegroundColor Yellow
Write-Host "  scan-sensors                  # Scan all sensors once"
Write-Host "  scan-sensors --loop          # Continuous scanning"
Write-Host "  scan-sensors --sensors 1 2   # Scan specific sensors"
Write-Host "  scan-sensors --help          # Show all options"
