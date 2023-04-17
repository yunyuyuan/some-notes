# Git Domain Map User

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