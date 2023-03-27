import argparse
from re import sub
import readline
import requests
from urllib.parse import urljoin

class LiveServerSession(requests.Session):
    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, **kwargs)

def get_args():
    parser = argparse.ArgumentParser(
                    prog = 'QBittorent Batch Rename',
                    epilog = '')
    parser.add_argument('-u', '--url', required=True)
    parser.add_argument('-c', '--cookie', required=True)
    args = parser.parse_args()
    return args

def batch_rename(source, dist, files):
    replace_map = [item for item in ([item, sub(source, dist, item)] for item in files) if item[0] != item[1]]
    results = [x[1] for x in replace_map]
    print('Preview:')
    for pair in replace_map:
        print(f'{pair[0]} -> {pair[1]}')
    if any(results.count(item) > 1 for item in results):
        print('Error!!!There is a file with the same name in the result. Aborting.')
        exit()
    confirm = input('Confirm?(y/N)')
    if confirm.lower() == 'y':
        return replace_map
    return []

if __name__ == '__main__':
    args = get_args()
    with LiveServerSession(args.url) as s:
        s.headers = {
            "Cookie": args.cookie
        }
        resp = s.post("/api/v2/sync/maindata")
        if resp.ok:
            torrents = resp.json()['torrents']
            hashs = list(torrents.keys())
            if not hashs:
                print("no torrent found.")
                exit()
            for idx,hash in enumerate(hashs):
                print(f'{idx+1}. {torrents[hash]["name"]}')
            index = None
            while index is None:
                index = input("Please select one > ")
                try:
                    index = int(index)-1
                    index = index if 0 <= index < len(hashs) else None
                except:
                    index = None
            selected_hash = hashs[index]
            selected_item = torrents[selected_hash]
            resp = s.get('/api/v2/torrents/files', params={"hash": selected_hash})
            if resp.ok:
                files = [x['name'] for x in resp.json()]
                for file in files:
                    print(file)
                source = input("Please input regex source > ")
                dist = input("Please input regex dist > ")
                replace_map = batch_rename(source, dist, files)
                if replace_map:
                    for pair in replace_map:
                        s.post('/api/v2/torrents/renameFile', {
                            "hash": hash,
                            "oldPath": pair[0],
                            "newPath": pair[1]
                        })
                    print('Succeed!')