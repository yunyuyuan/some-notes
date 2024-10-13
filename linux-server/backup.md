# Files Backup

## Need to backup
* `/etc`
* `/home`
* `/boot`
* `/root`
* `/var/www`
* `/data`
* mariaDB
* optional:
  * `/opt`

## Use tar to backup

::: tip
[`jq`](https://stedolan.github.io/jq/) needs to be installed first.
:::

```sh
vim /home/yunyuyuan/my-backup.sh
```
```sh
###### 
# Change this:
USER=yunyuyuan
USER_DIR=/home/$USER
BACKUP_DIR=$USER_DIR/backups
# Retain the 5 most recent backup files
MAX_BACKUP_FILE_COUNT=5
# Backup-To-Remote Function, my remote is nextcloud
backup_to_remote() {
  # REMOTE_DIR=nextcloud:/arch-backups
  REMOTE_DIR=/mnt/HDD/arch-backups
  LOCAL_LIST=($(rclone lsjson $BACKUP_DIR | jq -r '.[].Name'))
  REMOTE_LIST=($(rclone lsjson $REMOTE_DIR | jq -r '.[].Name'))
  
  # Purge the files present at remote but not present at local
  for element in "${REMOTE_LIST[@]}"; do
    if ! [[ " ${LOCAL_LIST[@]} " =~ " ${element} " ]]; then
      FILE=$REMOTE_DIR/$element
      echofunc "Deleting remote file <$FILE>"
      rclone delete $FILE
    fi
  done
  echofunc "Copying to remote ${REMOTE_DIR}"
  rclone copy $BACKUP_DIR $REMOTE_DIR --ignore-existing
}
######
if ! command -v jq &> /dev/null
then
  echo "'jq' is not installed. Please install it."
  exit 1
fi

# change work dir to /
cd /

echofunc() {
  echo "$(date +"%Y-%m-%d %T") <----- $1 ----->"
}

if ! [[ -e $BACKUP_DIR ]]; then
  echofunc "Creating backupdir: $BACKUP_DIR"
  mkdir -m 744 $BACKUP_DIR
fi

# create backup.tar
BACKUP_FILE=$BACKUP_DIR/backup_$(date +"%Y-%m-%d_%H-%M-%S").tar.gz
echofunc "Creating backup <$BACKUP_FILE>"
tar \
  --exclude="$BACKUP_DIR" \
  --exclude="/dev" \
  --exclude="/mnt" \
  --exclude="/proc" \
  --exclude="/sys" \
  --exclude="/tmp" \
  --exclude="/media" \
  --exclude="/btrbk_snapshots" \
  --exclude="/var/lib/docker" \
  --exclude="**/lost+found" \
  --exclude="**/cache" \
  --exclude="**/.cache" \
  --exclude="**/tmp" \
  --exclude="**/*.log" \
  --exclude="**/*.log.*" \
  --exclude="$USER_DIR/go" \
  --exclude="$USER_DIR/.nvm" \
  --exclude="$USER_DIR/.arduino*" \
  --exclude="$USER_DIR/.local/share/pnpm" \
  --exclude="$USER_DIR/.npm" \
  --exclude="$USER_DIR/.nuget" \
  --exclude="$USER_DIR/.vscode-server" \
  --exclude="/data/next-cloud/data/**/preview" \
  --exclude="/data/next-cloud/data/**/files_trashbin" \
  --exclude="/data/jellyfin/config/data/metadata/library" \
  --exclude="/data/jellyfin/config/data/transcodes" \
  --exclude="/data/immich/library/thumbs" \
  --exclude="/data/immich/library/encoded-video" \
  -czf $BACKUP_FILE \
  /

# remove oldest backup.tar
REMOVE_COUNT=$(($(ls $BACKUP_DIR | wc -l ) - $MAX_BACKUP_FILE_COUNT))
if (($REMOVE_COUNT > 0));then
  echofunc "Removing <$REMOVE_COUNT> oldest backups"
  cd $BACKUP_DIR 
  rm "$(ls $BACKUP_DIR -t | tail -$REMOVE_COUNT)"
fi
chown -R $USER $BACKUP_DIR

# sync all backup.tar to External Driver or Cloud Driver
echofunc "Running <backup_to_remote>"
backup_to_remote
```
## crontab task
```sh
sudo crontab -e
```
```sh
0 0 5 * * sh /home/yunyuyuan/my-backup.sh >> /var/log/my-backup.log
```

::: info 
Recommended to use `logrotate` to control the size of the log.
:::
## Whole System Backup
TODO