# Rclone snippets

## set master password for a new computer
```bash
> rclone config
> s) Set configuration password
```

## mount crypt
```bash
rclone mount my-encrypted: ~/Encrypted --vfs-cache-mode=full
```