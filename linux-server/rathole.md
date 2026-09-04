# OpenWRT

```
➜  ~ vim /etc/init.d/rathole-client                                                                                                                                                   
#!/bin/sh /etc/rc.common

START=99
STOP=10

USE_PROCD=1

PROG=/usr/bin/rathole
CONFIG=/etc/rathole.toml

start_service() {
    procd_open_instance rathole-client
    procd_set_param command "$PROG" "$CONFIG"
    procd_set_param respawn 3600 5 5
    procd_set_param stdout 1
    procd_set_param stderr 1
    procd_set_param file "$CONFIG"
    procd_close_instance
}

reload_service() {
    stop
    start
}

service_triggers() {
    procd_add_reload_trigger "rathole"
}
```