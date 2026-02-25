# Deploy updated Flask app with IPv6 support and restart service

Write-Host "Uploading updated app.py..." -ForegroundColor Green

# Copy app.py to Pi
scp -o StrictHostKeyChecking=no (Resolve-Path C:\Downloads\mushroom\app.py) mushroom@raspberrypi.local:/home/mushroom/mushroom_project/app.py

Write-Host "Restarting Flask service..." -ForegroundColor Green

# Restart the service
ssh -o StrictHostKeyChecking=no mushroom@raspberrypi.local "sudo systemctl restart substrate.service"

Write-Host "Waiting 3 seconds for service to start..." -ForegroundColor Green  
Start-Sleep -Seconds 3

# Check status
Write-Host "Checking service status..." -ForegroundColor Green
ssh -o StrictHostKeyChecking=no mushroom@raspberrypi.local "systemctl status substrate.service | head -15"

Write-Host "Testing Flask on localhost..." -ForegroundColor Green
ssh -o StrictHostKeyChecking=no mushroom@raspberrypi.local "curl -I http://127.0.0.1:5000 2>&1 | head -5"

Write-Host "`nDeployment complete! Dashboard should now be accessible at:" -ForegroundColor Cyan
Write-Host "  http://raspberrypi.local:5000" -ForegroundColor Yellow
Write-Host "  http://192.168.10.2:5000" -ForegroundColor Yellow
