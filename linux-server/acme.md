# acme.sh

## Install acme.sh
```sh
curl https://get.acme.sh | sh -s email=me@yunyuyuan.net
```

## Export DNS Api Key&Token to `rc` file
```sh
vim ~/.zshrc
export CF_Key=***
export CF_Token=***
source ~/.zshrc
```

## Obtain the certification
```
/home/yunyuyuan/.acme.sh/acme.sh --issue --dns dns_cf  -d '*.yunyuyuan.net' --force --server letsencrypt
```

## Create crontab to renew certification 
```sh
crontab -e
```
```sh
0 0 1 * * /home/yunyuyuan/.acme.sh/acme.sh --issue --dns dns_cf  -d '*.yunyuyuan.net' --force --server letsencrypt > /dev/null
```

## Create sudo crontab to restart nginx
```sh
sudo crontab -e
```
```sh
10 0 1 * * /usr/bin/nginx -s reload > /dev/null
```