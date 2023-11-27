# Git multiple users

# 1. Different user email/name for different remote

## Matching the specific domain
```sh
vim ~/.gitconfig
```
```ini
[user]
	name = yunyuyuan
	email = me@yunyuyuan.net

[includeIf "hasconfig:remote.*.url:git@git.example.com:*/**"]
    path = .gitconfig-another
```
## Add a configuration
```sh
vim ~/.gitconfig-another
```
```ini
[user]
	name = another-user
	email = another@yunyuyuan.net
```

# 2. Different identity for specific user

## Generate a new identity
```sh
ssh-keygen -f ~/.ssh/id_rsa_another
```

## Config the magic Host
```sh
vim ~/.ssh/config
```
```ini
# default user
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa

Host github.com-another
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa_another
```

## Then use this to `git clone`:
```sh
git clone git@github.com:default_user/xxx.git
git clone git@github.com-another:another_user/xxx.git
```

# 3. Custom SSH port
```sh
vim ~/.ssh/config
```
```ini
Host git.example.com
  HostName git.example.com
  User git
  Port 222
```