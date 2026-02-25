#!/bin/bash
# Deploy updated app.py and restart Flask service

# Upload the file
scp -o StrictHostKeyChecking=no C:/Downloads/mushroom/app.py mushroom@raspberrypi.local:/home/mushroom/mushroom_project/app.py

# Restart the service  
ssh -o StrictHostKeyChecking=no mushroom@raspberrypi.local "sudo systemctl restart substrate.service && sleep 2 && systemctl status substrate.service"

echo "Deployment complete!"
