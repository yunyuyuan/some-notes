# Vscode in browser

## Install
```sh
yay -S code-server
```

## Config
```sh
vim /data/code-server/config/config.yaml
```
```sh
bind-addr: 127.0.0.1:8112
auth: password
password: "123456"
cert: false
user-data-dir: /data/code-server/config/data
extensions-dir: /data/code-server/config/extensions
```

## Make a service
```sh
sudo vim /etc/systemd/system/code-server.service

[Unit]
Description=code server

[Service]
User=yunyuyuan
ExecStart=/usr/bin/code-server --config /data/code-server/config/config.yaml

[Install]
WantedBy=default.target
```