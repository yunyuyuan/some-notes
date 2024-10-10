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
MARIADB_FILE=mariadb.sql
MARIADB_APP=mariadb-app
MARIADB_USER=root
MARIADB_PWD=xxx
NEED_BACKUP="/etc /home /boot /root /var/www /var/spool /data"
# Retain the 5 most recent backup files
MAX_BACKUP_FILE_COUNT=5
# Backup-To-Remote Function, my remote is nextcloud
backup_to_remote() {
  REMOTE_DIR=nextcloud:/path/to/mybackupdir
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
  echofunc "Copying to remote"
  rclone copy $BACKUP_DIR $REMOTE_DIR --ignore-existing
}
######

# change work dir to /
cd /

echofunc() {
  echo "$(date +"%Y-%m-%d %T") <----- $1 ----->"
}

if ! [[ -e $BACKUP_DIR ]]; then
  echofunc "Creating backupdir: $BACKUP_DIR"
  mkdir -m 744 $BACKUP_DIR
fi

# create mariadb.sql
echofunc "Creating MariaDB backup"
docker exec $MARIADB_APP /usr/bin/mysqldump -h '127.0.0.1' -u $MARIADB_USER --password=$MARIADB_PWD --all-databases --routines --triggers --events > $MARIADB_FILE

# create backup.tar
BACKUP_FILE=$BACKUP_DIR/backup_$(date +"%Y-%m-%d_%H-%M-%S").tar.gz
echofunc "Creating backup <$BACKUP_FILE>"
tar \
  --exclude="$BACKUP_DIR" \
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
  --exclude="/data/immich" \
  -czf $BACKUP_FILE \
  $NEED_BACKUP $MARIADB_FILE

# remove backup.sql
echofunc "Removing <$MARIADB_FILE>"
rm "$MARIADB_FILE"

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
## restore mysql
```sh
docker exec mariadb-app /usr/bin/mysqldump -h '127.0.0.1' -u $MARIADB_USER --password=$MARIADB_PWD --all-databases --routines --triggers --events > mariadb.sql
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