# netdata system monitor

## HDD Temperature
```sh
sudo vim /etc/smartd.conf

/dev/sda -a -d sat
/dev/sdb -a -d sat
```
```sh
sudo systemctl enable --now smartd.service
```

```sh
sudo /etc/netdata/edit-config /etc/netdata/python.d/smartd_log.conf

local:
  name: smartd_log
  log_path: '/var/log/smartd/'
```