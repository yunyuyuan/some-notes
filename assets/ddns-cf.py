import time
import socket
import requests
import subprocess

import logging
from logging.handlers import RotatingFileHandler

config = {
    "api_token": "xxx",
    "api_key": "xxx",
    "account_email": "xxx@example.com",
    "zone_id": "xxx",
    "lan_ipv4": "192.168.1.123", # LAN ipv4 for vpn networking
    "cname_target": "i", # set all domain as a CNAME of i-d.yourdomain.com for ipv6 and i-v.yourdomain.com for LAN ipv4
    "domain_name": [
        {
            # direct will be: i-d.yourdomain.net
            # vpn will be: i-v.yourdomain.net
            "name": "i",
        },{
            "name": "file",
        },{
            "name": "video",
        }],
}
logFile = '/home/yunyuyuan/ddns/ddns.log'

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')


my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=1024*1024,
                                 backupCount=2, encoding=None, delay=False)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)

def get_dynamic_ipv6_address(interface="eth0"):
    try:
        # Run the 'ip -6 addr show' command to get the IPv6 address for the interface
        result = subprocess.run(['ip', '-6', 'addr', 'show', interface], capture_output=True, text=True, check=True)
        
        # Extract lines containing 'inet6' and scope global
        lines = result.stdout.split('\n')
        for line in lines:
            if 'inet6' in line and 'scope global' in line:
                # Extract the IPv6 address part
                address = line.split()[1].split('/')[0]
                return address
    except subprocess.CalledProcessError as e:
        app_log.error(f"Failed to get IPv6 address for interface {interface}. Error: {e}")
    return None

## for Windows
# def get_dynamic_ipv6_address():
#     file = path.abspath('ipv6.ps1') # content of ipv6.ps1:  Get-NetIPAddress -AddressFamily IPv6 | Where-Object { $_.PrefixOrigin -eq 'RouterAdvertisement' -and $_.AddressState -eq 'Preferred' }
#     output = str(subprocess.Popen(['powershell.exe', file], stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])
#     for item in output.split('\n\n'):
#         ip: re.Match = re.search('IPAddress\s*:\s*([0-9a-zA-Z:]+)', item)
#         interface: re.Match = re.search('InterfaceAlias\s*:\s*(.+)', item)
#         prefix_length: re.Match = re.search('PrefixLength\s*:\s*(\d+)', item)
#         if ip and interface.groups()[0].lower() == 'wlan' and prefix_length.groups()[0] == '64':
#             return ip.groups()[0]

def get_ip(ip_type):
    if ip_type == 'LOCAL':
        return config['lan_ipv4']
    elif ip_type == 'A':
        return requests.get('https://4.ipw.cn').text
    return get_dynamic_ipv6_address()

def cf_api(endpoint, method, headers={}, data=False):
    api_token = config['api_token']
    if api_token != '' and api_token != 'api_token_here':
        headers = {
            "Authorization": "Bearer " + api_token, **headers
        }
    else:
        headers = {
            "X-Auth-Email": config['account_email'],
            "X-Auth-Key": config['api_key'],
        }
    try:
        if(data == False):
            response = requests.request(method, "https://api.cloudflare.com/client/v4/" + endpoint, headers=headers)
        else:
            response = requests.request(
                method, "https://api.cloudflare.com/client/v4/" + endpoint,
                headers=headers, json=data)

        if response.ok:
            return response.json()
        else:
            app_log.error("Error sending '" + method +
                  "' request to '" + response.url + "':" + response.text)
            return None
    except Exception as e:
        app_log.error("An exception occurred while sending '" +
              method + "' request to '" + endpoint + "': " + str(e))
        return None

def call_api(domain_suffix, c_domain, domain_type):
    is_cname_target = c_domain["name"] == config["cname_target"]
    real_type = ('A' if domain_type == 'LOCAL' else domain_type) if is_cname_target else "CNAME"
    domain_name = c_domain["name"] + domain_suffix
    domain_content = get_ip(domain_type) if is_cname_target else (config["cname_target"] + domain_suffix)
    record = {
        "type": real_type,
        "name": domain_name,
        "content": domain_content,
        "proxied": False,
        "ttl": 1
    }
    dns_records = cf_api("zones/" + config['zone_id'] + f"/dns_records?per_page=100&type={real_type}&name={domain_name}", "GET")
    response = {}
    if dns_records['result']:
        # updating
        app_log.info(f'updating {domain_name} with {domain_content}')
        dns_record = dns_records['result'][0]
        if dns_record['content'] == record['content']:
            app_log.info(f'local ip: {record["content"]} same to server, no need to update.')
        else:
            response = cf_api("zones/" + config['zone_id'] + "/dns_records/" + dns_record['id'], "PUT", {}, record)
    else:
        # creating
        app_log.info(f'creating {domain_name} with {domain_content}')
        response = cf_api("zones/" + config['zone_id'] + "/dns_records", "POST", {}, record)
    if response and response.get('success', None):
        app_log.info(f'succeeded set ip to: {record["content"]}.')

def ddns():
    response = cf_api("zones/" + config['zone_id'], "GET")
    if response is None or response["result"]["name"] is None:
        app_log.error(f'get domain info error with zones api')
        return
    zone_result_name = response["result"]["name"]
    for c_domain in config["domain_name"]:
        call_api('-d.' + zone_result_name, c_domain, 'AAAA')
        if config['lan_ipv4']:
            call_api('-v.' + zone_result_name, c_domain, 'LOCAL')

if __name__ == '__main__':
    try:
        ddns()
    except Exception as e:
        app_log.error(f'error: {str(e)}')
    
    # import time
    # while True:
    #     try:
    #         ddns()
    #     except Exception as e:
    #         app_log.error(f'error: {str(e)}')
        
    #     time.sleep(600)