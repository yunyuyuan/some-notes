# openwrt

## Backup whole system(`/overlay`)
```sh
tar -cvzf /tmp/overlay.tar.gz /overlay
```
Then save `/tmp/overlay.tar.gz` as your backup.
## Restore
```sh
firstboot && reboot now
cd /; tar -xvzf /tmp/overlay.tar.gz
```