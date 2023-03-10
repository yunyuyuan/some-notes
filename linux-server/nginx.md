# Nginx

## Nginx auth_basic
```sh
sudo sh -c "echo -n 'yunyuyuan:' >> /etc/nginx/auth-pairs"
sudo sh -c "openssl passwd -apr1 >> /etc/nginx/auth-pairs"
```

## Nginx conf
<<< @/linux-server/nginx.conf{nginx}