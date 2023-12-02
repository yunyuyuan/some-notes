import time
import socket
import requests

import logging
from logging.handlers import RotatingFileHandler

config = {
    "api_token": "xxx",
    "api_key": "xxx",
    "account_email": "xxx@example.com",
    "zone_id": "xxx",
    "lan_ipv4": "192.168.1.123", # for vpn networking
    "domain_name": [
        {
            # direct will be: i-d.example.net
            # vpn will be: i-v.example.net
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

def get_ipv6_address():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        
        # Connect to a remote server (doesn't actually send data)
        s.connect(("v2ray-sw-d.yunyuyuan.net", 80))
        
        # Get the global IPv6 address from the connected socket
        ipv6_address = s.getsockname()[0]
        
        return ipv6_address
    except Exception as e:
        app_log.error(f"Error: {e}")
        return None

def get_ip(ip_type):
    if ip_type == 'LOCAL':
        return config['lan_ipv4']
    elif ip_type == 'A':
        return requests.get('https://4.ipw.cn').text
    return get_ipv6_address()

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
                  "' request to '" + response.url + "':")
            return None
    except Exception as e:
        app_log.error("An exception occurred while sending '" +
              method + "' request to '" + endpoint + "': " + str(e))
        return None

def call_api(domain_name, c_domain, domain_type):
    record = {
        "type": 'A' if domain_type == 'LOCAL' else domain_type,
        "name": domain_name,
        "content": get_ip(domain_type),
        "proxied": False,
        "ttl": 1
    }
    dns_records = cf_api("zones/" + config['zone_id'] + f"/dns_records?per_page=100&type={domain_type}&name={domain_name}", "GET")
    response = {}
    if dns_records['result']:
        # updating
        app_log.info(f'updating {domain_name}')
        dns_record = dns_records['result'][0]
        if dns_record['content'] == record['content']:
            app_log.info(f'local ip: {record["content"]} same to server, no need to update.')
        else:
            response = cf_api("zones/" + config['zone_id'] + "/dns_records/" + dns_record['id'], "PUT", {}, record)
    else:
        # creating
        app_log.info(f'creating {domain_name}')
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
        call_api(c_domain["name"] + '-d.' + zone_result_name, c_domain, 'AAAA')
        if config['lan_ipv4']:
            call_api(c_domain["name"] + '-v.' + zone_result_name, c_domain, 'LOCAL')

if __name__ == '__main__':
    try:
        ddns()
    except Exception as e:
        app_log.error(f'error: {str(e)}')