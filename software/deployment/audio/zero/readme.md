# Overview 

A python files is deployed and conigured as a service to the Pi for audio.
Pi Zero is controlled via a serial port from the Pico.

## Install the service

The examples below assume the Linux account is pi. If your Pi Zero uses another account, change the paths and User= accordingly.

Create the directories and install the serial dependency:

# To Configure the Pi Zero:

```
sudo mkdir -p /opt/dabones-audio
sudo mkdir -p /home/sparky/audio/

sudo apt update
sudo apt install -y python3-serial alsa-utils
```

Copy audio_service.py to /opt/dabones-audio/audio_service.py, then set ownership and permissions:

```
sudo chown root:root /opt/dabones-audio/audio_service.py
sudo chmod 755 /opt/dabones-audio/audio_service.py

sudo chown -R sparky:sparky /home/sparky/audio/
```

Place your audio files in /home/sparky/audio/, for example 1.wav. The program uses the filename you send; it does not require numbered songs.

## systemd unit

Save as /etc/systemd/system/dabones-audio.service.

```
[Unit]
Description=DaBones Audio Playback Service
After=sound.target

[Service]
Type=simple
User=pi
SupplementaryGroups=audio dialout
WorkingDirectory=/opt/dabones-audio

Environment=DABONES_SERIAL_PORT=/dev/serial0
Environment=DABONES_BAUD_RATE=115200
Environment=DABONES_SONG_DIR=/home/sparky/audio/
Environment=DABONES_APLAY=/usr/bin/aplay

ExecStart=/usr/bin/python3 /opt/dabones-audio/audio_service.py

Restart=on-failure
RestartSec=2

NoNewPrivileges=true
ProtectSystem=full
ProtectHome=read-only

[Install]
WantedBy=multi-user.target
```

Install and start the service:

```
sudo systemctl daemon-reload
sudo systemctl enable --now dabones-audio.service
```

Check whether it started:

```
sudo systemctl status dabones-audio.service
```

View live logs:

```
sudo journalctl -u dabones-audio.service -f
```

Restart after changing the configuration:

```
sudo systemctl restart dabones-audio.service
```

# UART setup

Because the UART is now an application protocol rather than a terminal, make sure Linux isn't also using it for a login shell.

1. Run readlink -f /dev/serial0 to identify the underlying UART device.
2. In Raspberry Pi configuration, enable the UART hardware and disable the serial login shell.
3. Ensure the corresponding serial-getty@... service is stopped and disabled for that device.
4. Reboot and verify that the audio service starts successfully.

Do not disable the UART hardware itself; only disable the console/login service.

#
# -> sudo raspi-config
#
# Navigate to Interface Options → Serial Port. Select:
# - Login shell accessible over serial? → Yes
# - Serial port hardware enabled? → Yes
# - Finish
#
# -> sudo reboot
#
# Serial Settings:
# Baud rate	    115200
# Data bits	    8
# Parity	    None
# Stop bits	    1
# Flow control	None