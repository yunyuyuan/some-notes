# netdata system monitor

## HDD Temperature
```sh
~ ᐅ sudo vim /etc/smartd.conf

/dev/sda -a -d sat
/dev/sdb -a -d sat
```

```sh
~ ᐅ sudo vim /etc/conf.d/smartd 
SMARTD_ARGS="-A /var/log/smartd/ -i 300"
```

```sh
sudo systemctl enable --now smartd.service
```

```sh
~ ᐅ sudo /etc/netdata/edit-config /etc/netdata/python.d/smartd_log.conf

local:
  name: smartd_log
  log_path: '/var/log/smartd/'
```