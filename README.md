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
ExecStart=/home/pi/roomba/env/bin/python3 /home/pi/roomba/test980_bot.py
Restart=on-failure
RestartSec=5s
[Install]
WantedBy=multi-user.target
```

sudo systemctl enable roombot

sudo vim /etc/systemd/system/rest980.service

```
[Unit]
Description=rest980
[Service]
Type=simple
PIDFile=/run/rest980.pid
User=pi
Group=pi
WorkingDirectory=/home/pi/rest980
ExecStart=npm start
Restart=on-failure
RestartSec=5s
[Install]
WantedBy=multi-user.target
```

sudo systemctl enable rest980