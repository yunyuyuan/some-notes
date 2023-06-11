# aria2

## Install aria2
```sh
yay -S aria2
```

## Create configuration file
```sh
vim ~/.config/aria2.conf
```
```ini
continue
daemon=true
dir=/home/yunyuyuan
rpc-allow-origin-all=true
file-allocation=falloc
log-level=warn
# touch /var/log/aria2.log and use chown to make sure that current user can access /var/log/aria2.log
log=/var/log/aria2.log
max-connection-per-server=16
split=16
max-concurrent-downloads=5
max-overall-download-limit=0
min-split-size=5M
enable-http-pipelining=true
allow-overwrite=true
follow-torrent=false

enable-rpc=true
rpc-listen-all=true
rpc-secret=xxxxxxxxxxxxx
#check-certificate=false
```

## Create systemd service
```sh
sudo vim /etc/systemd/system/aria2.service
```
```ini
[Unit]
Description=aria2 Daemon

[Service]
Type=forking
User=yunyuyuan
ExecStart=/usr/bin/aria2c --conf-path=/home/yunyuyuan/.config/aria2.conf

[Install]
WantedBy=default.target
```
Start & Enable service
```sh
sudo systemctl enable --now aria2.service
```

## WebUI for linux server
> [Aria2Ng install guide](https://github.com/mayswind/AriaNg#installation)  

**Nginx reverse proxy**:
```nginx
server {
    listen 80;
    server_name aria.yunyuyuan.net;

    root /var/www/aria;
    location /jsonrpc {
        proxy_pass http://localhost:6800/jsonrpc;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```