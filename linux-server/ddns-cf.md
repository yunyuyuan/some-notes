# DDNS for cloudflare

## Code
<<< @/assets/ddns-cf.py

## Make a systemd service
```sh
sudo vim /etc/systemd/system/pyddns.service
```
```ini
[Unit]
Description=CloudFlare DDNS
After=network-online.target syslog.target

[Service]
User=yunyuyuan
ExecStart=/usr/bin/python3 /home/yunyuyuan/ddns/ddns-cf.py
RestartSec=300
Restart=always

[Install]
WantedBy=multi-user.target

```
```sh
sudo systemctl enable --now pyddns.service
```