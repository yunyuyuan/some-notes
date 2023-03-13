# Cloudflared tunnel

## Install cloudflared
```sh
# for arch linux
yay -S cloudflared
```

::: info
If you are using another distro, please refer [install guide](https://github.com/cloudflare/cloudflared/#installing-cloudflared).
:::

## Create tunnel
```sh
cloudflared tunnel login
cloudflared tunnel create my-tunnel
```
Then, use `cloudflared tunnel list` to show **ID** of **my-tunnel**:
```sh
~ $ cloudflared tunnel list
ID                                   NAME    CREATED              CONNECTIONS
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx my-tunnel 2023-01-08T02:26:41Z 2xLAX, 2xSJC
```

## Create config.yml
```sh
vim ~/.cloudflared/config.yml
```
```yml
tunnel: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
credentials-file: /home/yunyuyuan/.cloudflared/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.json
ingress:
  - hostname: ssh.yunyuyuan.net
    service: ssh://localhost
  - hostname: vnc.yunyuyuan.net
    service: tcp://localhost:5900
  - hostname: git.yunyuyuan.net
    service: http://localhost:7654
  - hostname: git-ssh.yunyuyuan.net
    service: ssh://localhost:222
  - hostname: file.yunyuyuan.net
    service: http://localhost:80
  - hostname: aria.yunyuyuan.net
    service: http://localhost:80
  - service: http_status:404
```

## Create tunnel&DNS script
```sh
vim ~/tunnel-dns.sh
```
```sh
# update cloudflare DNS record
/usr/bin/cloudflared tunnel route dns my-tunnel git.yunyuyuan.net
/usr/bin/cloudflared tunnel route dns my-tunnel git-ssh.yunyuyuan.net
/usr/bin/cloudflared tunnel route dns my-tunnel ssh.yunyuyuan.net
/usr/bin/cloudflared tunnel route dns my-tunnel vnc.yunyuyuan.net
/usr/bin/cloudflared tunnel route dns my-tunnel file.yunyuyuan.net
/usr/bin/cloudflared tunnel route dns my-tunnel aria.yunyuyuan.net
# run tunnel
/usr/bin/cloudflared tunnel run my-tunnel
```

## Create tunnel service
```sh
sudo vim /etc/systemd/system/cloudflared-tunnel.service
```
```service
[Unit]
Description=cloudflared tunnel
Requires=network-online.target 
After=network-online.target
StartLimitInterval=300

[Service]
User=yunyuyuan
ExecStart=sh /home/yunyuyuan/tunnel-dns.sh
# auto retry, because cloudflare's DNS 1.1.1.1 maybe failure after boot.
Restart=always
RestartSec=30

[Install]
WantedBy=default.target
```
Start & Enable service
```sh
sudo systemctl enable --now cloudflared-tunnel.service
```

## Client-side Usage

#### SSH config
```ini
Host ssh.yunyuyuan.net
  ProxyCommand D:\\tools\\cloudflared-windows-amd64.exe access ssh --hostname %h
```

#### VNC tunnel
```sh
cloudflared access tcp --hostname vnc.yunyuyuan.net --url tcp://localhost:5901
```

#### Git
```ini
Host ssh.yunyuyuan.net git-ssh.yunyuyuan.net
  ProxyCommand D:\\tools\\cloudflared-windows-amd64.exe access ssh --hostname %h
```

```sh
# through tunnel
git clone git@git-ssh.yunyuyuan.net:yunyuyuan/self-host-starter.git
# through pure ipv6
git clone ssh://git@<youripv6>:222/yunyuyuan/self-host-starter.git
```

Multiple remotes
```ini
[remote "github"]
  url = git@github.com:yunyuyuan/self-host-starter.git
  fetch = +refs/heads/*:refs/remotes/github/*
[remote "gitea"]
  url = git@git-ssh.yunyuyuan.net:yunyuyuan/self-host-starter.git
  fetch = +refs/heads/*:refs/remotes/gitea/*
[remote "origin"]
  url = git@github.com:yunyuyuan/self-host-starter.git
  url = git@git-ssh.yunyuyuan.net:yunyuyuan/self-host-starter.git
```