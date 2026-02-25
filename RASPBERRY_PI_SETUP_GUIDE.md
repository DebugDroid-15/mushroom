# Complete Raspberry Pi Setup Guide - Substrate Monitoring System

## Prerequisites
- Raspberry Pi 4B (or later) with 4GB+ RAM recommended
- SD Card (32GB+ recommended)
- USB power adapter (5V 3A minimum)
- Ethernet cable for LAN connection
- Computer with SD card reader
- Monitor, HDMI cable, and keyboard/mouse (or SSH capability)

---

## PHASE 1: OS Installation & Initial Setup

### Step 1.1: Download & Flash Raspberry Pi OS

**On Your Windows Computer:**

1. Download **Raspberry Pi Imager** from: https://www.raspberrypi.com/software/
2. Download **Raspberry Pi OS (Bookworm)** - 64-bit recommended
3. Insert SD card into card reader
4. Open Raspberry Pi Imager
5. Select OS → Raspberry Pi OS (64-bit) → Storage → Your SD Card
6. Click **Write** (will take 5-10 minutes)
7. Eject SD card safely

### Step 1.2: First Boot

1. Insert SD card into Raspberry Pi
2. Connect Ethernet cable to Pi and router
3. Connect HDMI monitor and keyboard/mouse
4. Power on Pi (will take 1-2 minutes to boot)
5. Complete initial setup wizard when prompted:
   - Select language/timezone
   - Create username (e.g., `mushroom`) and password
   - Configure WiFi (optional for now, can skip)
   - Update software when prompted

---

## PHASE 2: Network Configuration (LAN)

### Step 2.1: Verify LAN Connection

Open Terminal and run:
```bash
ip addr show eth0
```

You should see an IP address like `192.168.x.x`. Note this IP address.

### Step 2.2: Enable SSH (for remote access)

```bash
sudo raspi-config
```

Navigate to:
- Interface Options → SSH → Yes
- Exit and reboot

```bash
sudo reboot
```

**After reboot**, you can connect via SSH from your computer:
```bash
ssh mushroom@192.168.x.x
```
(Replace 192.168.x.x with your Pi's IP address from Step 2.1)

### Step 2.3: Static IP Configuration (Recommended)

This prevents the Pi from getting a different IP each time it reboots.

```bash
sudo nano /etc/dhcpcd.conf
```

Scroll to bottom and add (adjust your network values):
```bash
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 8.8.4.4
```

Press `Ctrl+O` → `Enter` → `Ctrl+X`

```bash
sudo reboot
```

After reboot, your Pi will always be at `192.168.1.100` (adjust if needed)

---

## PHASE 3: System Updates & Python Setup

### Step 3.1: Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

(This may take 5-10 minutes)

### Step 3.2: Install Python & Required Tools

```bash
sudo apt install -y python3 python3-pip python3-venv git
```

### Step 3.3: Create Virtual Environment

```bash
cd ~
python3 -m venv substrate_env
source substrate_env/bin/activate
```

**You should see `(substrate_env)` at the start of terminal lines now.**

### Step 3.4: Install Python Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install flask python-dotenv RPi.GPIO minimalmodbus PyYAML
```

Expected installation time: 2-3 minutes

---

## PHASE 4: Project Deployment

### Step 4.1: Create Project Directory

```bash
mkdir -p ~/mushroom_monitoring
cd ~/mushroom_monitoring
```

### Step 4.2: Transfer Project Files from Windows

**Option A: Using Git (Recommended)**

If you have your project on GitHub:
```bash
git clone https://github.com/YOUR_USERNAME/mushroom_monitoring.git
cd mushroom_monitoring
```

**Option B: Manual File Transfer (SCP)**

From your Windows computer (PowerShell):
```powershell
# First, copy your project folder to Pi
scp -r "C:\Downloads\mushroom\*" mushroom@192.168.1.100:~/mushroom_monitoring/
```

**Option C: Direct Copy (If using Monitor & Keyboard)**

Use text editor to create files directly on Pi:
```bash
nano app.py
# Copy-paste content from your computer
```

### Step 4.3: Verify File Structure

```bash
ls -la ~/mushroom_monitoring/
```

Expected files:
```
app.py
modbus_sensor.py
templates/
├── dashboard.html
dummy_dashboard.html
requirements.txt (optional)
config.yaml (optional)
```

---

## PHASE 5: GPIO & Hardware Configuration

### Step 5.1: Verify GPIO Access

```bash
sudo apt install -y python3-rpi.gpio
python3 << 'EOF'
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.LOW)
GPIO.cleanup()
print("GPIO test successful!")
EOF
```

### Step 5.2: Configure GPIO for Running Without sudo

```bash
sudo usermod -a -G gpio mushroom
sudo usermod -a -G spi mushroom
sudo usermod -a -G i2c mushroom
```

**Logout and login for changes to take effect:**
```bash
exit
```

Then SSH back in:
```bash
ssh mushroom@192.168.1.100
```

### Step 5.3: Enable I2C (for sensors if needed)

```bash
sudo raspi-config
```

Navigate to:
- Interface Options → I2C → Yes
- Exit

```bash
sudo reboot
```

Verify I2C:
```bash
sudo apt install -y i2c-tools
i2cdetect -y 1
```

---

## PHASE 6: Backend Service Setup

### Step 6.1: Navigate to Project

```bash
cd ~/mushroom_monitoring
source ~/substrate_env/bin/activate
```

### Step 6.2: Test Flask App

```bash
python3 app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

**Success!** The app is running. Keep it running for now.

### Step 6.3: Access Dashboard from Another Computer

On your Windows computer, open browser and go to:
```
http://192.168.1.100:5000
```

You should see your Substrate Monitoring Dashboard!

Press `Ctrl+C` in terminal to stop the app.

---

## PHASE 7: Automatic Startup Service

### Step 7.1: Create Systemd Service File

```bash
sudo nano /etc/systemd/system/substrate-monitor.service
```

Paste the following:
```ini
[Unit]
Description=Substrate Monitoring System
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=mushroom
WorkingDirectory=/home/mushroom/mushroom_monitoring
Environment="PATH=/home/mushroom/substrate_env/bin"
ExecStart=/home/mushroom/substrate_env/bin/python3 app.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Press `Ctrl+O` → `Enter` → `Ctrl+X`

### Step 7.2: Enable & Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable substrate-monitor.service
sudo systemctl start substrate-monitor.service
```

### Step 7.3: Verify Service is Running

```bash
sudo systemctl status substrate-monitor.service
```

You should see `active (running)` in green.

View real-time logs:
```bash
sudo journalctl -u substrate-monitor.service -f
```

(Press `Ctrl+C` to exit)

---

## PHASE 8: Hardware Verification

### Step 8.1: Verify Sensor Connection

With app running, check `/api/sensors` endpoint:

From Windows:
```powershell
Invoke-WebRequest -Uri "http://192.168.1.100:5000/api/sensors" | Select-Object -ExpandProperty Content
```

Or from Pi terminal:
```bash
curl http://localhost:5000/api/sensors
```

You should see JSON with sensor data (may show demo data if sensors not connected yet).

### Step 8.2: Test Humidifier GPIO

Ensure GPIO pins 23, 22, 25, 26 are connected to your humidifier relay module:

```python
python3 << 'EOF'
import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Test humidifier pins
pins = [23, 22, 25, 26]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Test each pin
for i, pin in enumerate(pins, 1):
    print(f"Testing Pin {pin} (Humidifier {i})...")
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.5)

print("GPIO test complete!")
GPIO.cleanup()
EOF
```

**Watch your humidifier outputs during test** - each should activate for 1 second.

---

## PHASE 9: Complete System Test

### Step 9.1: Verify Dashboard Loading

1. Navigate to `http://192.168.1.100:5000` in browser
2. Confirm all 4 sensors display on dashboard
3. Test sensor ON/OFF toggles (🟢/🔴 buttons)
4. Test humidifier toggles (✅/❌ buttons)
5. Verify alerts appear when toggling

### Step 9.2: Monitor Service Logs

```bash
sudo journalctl -u substrate-monitor.service -n 50
```

Check for any errors. Should show:
```
Substrate Monitor starting...
Flask app initialized
Sensor polling active
```

### Step 9.3: Performance Check

```bash
free -h           # Check RAM usage
df -h             # Check disk space
vcgencmd measure_temp  # Check CPU temperature
```

Everything should look healthy.

---

## PHASE 10: WiFi Configuration (For Later)

When ready to use WiFi instead of Ethernet:

### Step 10.1: Connect to WiFi

```bash
sudo raspi-config
```

Navigate to:
- System Options → Wireless LAN
- Select your country
- Enter WiFi network name (SSID)
- Enter WiFi password
- Exit and reboot

```bash
sudo reboot
```

### Step 10.2: Verify WiFi Connection

```bash
ip addr show wlan0
```

Note the new WiFi IP address. You can now:
- Disconnect Ethernet
- Connect to dashboard via WiFi IP address
- Access from anywhere in your house

### Step 10.3: Disable Ethernet (Optional)

If you prefer WiFi only:
```bash
sudo nano /etc/dhcpcd.conf
```

Find the eth0 section and comment it out with `#`:
```bash
#interface eth0
#static ip_address=192.168.1.100/24
```

---

## Troubleshooting

### Issue: Service won't start
```bash
sudo systemctl status substrate-monitor.service
sudo journalctl -u substrate-monitor.service -n 20
```

Check for Python module import errors.

### Issue: Dashboard shows "Disconnected"
```bash
curl http://localhost:5000/api/sensors
```

If this fails, Flask app isn't running. Check logs.

### Issue: GPIO Permission Denied
Ensure you ran:
```bash
sudo usermod -a -G gpio mushroom
```

And logged out/back in.

### Issue: Sensors show no data
1. Verify sensor wiring (RS-485, I2C, or Modbus as needed)
2. Check sensor power (12V for NPK sensors)
3. Verify I2C is enabled: `i2cdetect -y 1`
4. Check app.py sensor addresses match your devices

### Issue: Humidifier not triggering
1. Verify GPIO pins in app.py match your wiring
2. Test GPIO directly with the test script above
3. Check humidity threshold (should be <60% to trigger)
4. Verify relay module power

---

## Quick Command Reference

**Restart service:**
```bash
sudo systemctl restart substrate-monitor.service
```

**View logs:**
```bash
sudo journalctl -u substrate-monitor.service -f
```

**SSH into Pi:**
```bash
ssh mushroom@192.168.1.100
```

**Activate virtual environment:**
```bash
source ~/substrate_env/bin/activate
```

**Stop service:**
```bash
sudo systemctl stop substrate-monitor.service
```

**View system stats:**
```bash
vcgencmd measure_temp
vcgencmd get_throttled
```

---

## Dashboard Access

**Local Network:**
- `http://192.168.1.100:5000` (or your static IP)

**From another Pi:**
- `ssh mushroom@192.168.1.100`

**From Windows:**
- Browser: `http://192.168.1.100:5000`
- PowerShell: `Invoke-WebRequest http://192.168.1.100:5000`

---

## Next Steps

1. ✅ Follow Phase 1-4 to get OS and project running
2. ✅ Follow Phase 5-6 to configure GPIO and test backend
3. ✅ Follow Phase 7 to set up automatic startup
4. ✅ Follow Phase 8-9 to verify hardware and dashboard
5. 📝 Follow Phase 10 when ready for WiFi setup

**Estimated Total Setup Time: 30-45 minutes**

Good luck! 🍄
