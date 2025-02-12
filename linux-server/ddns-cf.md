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


## For Windows

#### ipv6.ps1
```ps
Get-NetIPAddress -AddressFamily IPv6 | Where-Object { $_.PrefixOrigin -eq 'RouterAdvertisement' -and $_.AddressState -eq 'Preferred' }
```

#### ddns.py
```python
# ......
def get_dynamic_ipv6_address():
    output = str(subprocess.Popen(['powershell.exe', path.abspath('ipv6.ps1')], stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])
    for item in output.split('\n\n'):
        ip: re.Match = re.search('IPAddress\s*:\s*([0-9a-zA-Z:]+)', item)
        interface: re.Match = re.search('InterfaceAlias\s*:\s*(.+)', item)
        prefix_length: re.Match = re.search('PrefixLength\s*:\s*(\d+)', item)
        if ip and interface.groups()[0].lower() in ['wlan', '以太网'] and prefix_length.groups()[0] == '64':
            return ip.groups()[0]
# ......
```

#### start.vbs
```vbs
CreateObject("WScript.Shell").Run "python D:\path\to\ddns.py",0
```