# roomba

### Service

sudo vim /etc/systemd/system/roombot.service

```
[Unit]
Description=roombot
[Service]
Type=simple
PIDFile=/run/roombot.pid
User=pi
Group=pi
WorkingDirectory=/home/pi/roomba
VIRTUAL_ENV=/home/pi/roomba/env/
Environment=PATH=$VIRTUAL_ENV/bin:$PATH
ExecStart=/home/pi/roomba/env/bin/python3 /home/pi/roomba/bot.py
Restart=on-failure
RestartSec=5s
[Install]
WantedBy=multi-user.target
```
