######
# Change this:
USER=yunyuyuan
USER_DIR=/home/$USER
# Restic repository via rclone backend
# RESTIC_REPOSITORY=rclone:nextcloud:/Nas/dev/home-arch-backups
RESTIC_REPOSITORY=rclone:teracloud:/home-arch-backup
# Password file for restic (chmod 600)
RESTIC_PASSWORD_FILE=$USER_DIR/.restic-password
# Local MariaDB dump dir (will be included in the restic snapshot)
DB_DUMP_DIR=/var/backups/mariadb
# Retention policy applied after each backup
RETENTION="--keep-daily 7 --keep-weekly 4 --keep-monthly 6"
######

export RESTIC_REPOSITORY
export RESTIC_PASSWORD_FILE

echofunc() {
  echo "$(date +"%Y-%m-%d %T") <----- $1 ----->"
}

# Check dependencies
for cmd in restic rclone; do
  if ! command -v $cmd &> /dev/null; then
    echo "'$cmd' is not installed. Please install it."
    exit 1
  fi
done

if [[ ! -r $RESTIC_PASSWORD_FILE ]]; then
  echo "Password file <$RESTIC_PASSWORD_FILE> is missing or unreadable."
  exit 1
fi

# Initialize repository on first run
if ! restic snapshots &> /dev/null; then
  echofunc "Initializing restic repository at $RESTIC_REPOSITORY"
  restic init
fi

# Dump MariaDB so the backup is consistent (live datafiles can't be tarred safely)
if command -v mariadb-dump &> /dev/null && systemctl is-active --quiet mariadb; then
  echofunc "Dumping MariaDB to $DB_DUMP_DIR"
  mkdir -p $DB_DUMP_DIR
  DUMP_FILE=$DB_DUMP_DIR/all-databases_$(date +"%Y-%m-%d").sql.gz
  mariadb-dump --all-databases --single-transaction --quick --lock-tables=false \
    | gzip > $DUMP_FILE
  # keep only the 3 latest dumps locally
  ls -t $DB_DUMP_DIR/all-databases_*.sql.gz | tail -n +4 | xargs -r rm
fi

# Exclude list (restic pattern syntax matches tar's globs closely)
EXCLUDE_FILE=$(mktemp)
cat > $EXCLUDE_FILE <<EOF
/dev
/mnt
/proc
/sys
/usr
/run
/tmp
/media
/btrbk_snapshots
/var/lib/docker
/var/log
$USER_DIR/backups
**/lost+found
**/node_modules
**/venv
**/.venv
**/cache
**/.cache
**/tmp
**/log
**/*.log
**/*.log.*
$USER_DIR/go
$USER_DIR/.nvm
$USER_DIR/.arduino*
$USER_DIR/.local/share/pnpm
$USER_DIR/.npm
$USER_DIR/.nuget
$USER_DIR/.vscode-server
/data/next-cloud/data/**/preview
/data/next-cloud/data/**/files_trashbin
/data/jellyfin/config/data/metadata/library
/data/jellyfin/config/data/transcodes
/data/immich/library/thumbs
/data/immich/library/encoded-video
/data/qbittorrent/downloads
EOF

# Run the backup
echofunc "Running restic backup"
restic backup / \
  --exclude-file=$EXCLUDE_FILE \
  --exclude-caches \
  --tag scheduled
BACKUP_RC=$?
rm $EXCLUDE_FILE

# Exit code 3 means "some files could not be read" - treat as warning, keep going
if [[ $BACKUP_RC -ne 0 && $BACKUP_RC -ne 3 ]]; then
  echofunc "restic backup failed with exit code $BACKUP_RC"
  exit $BACKUP_RC
fi

# Apply retention policy and prune unreferenced data
echofunc "Pruning old snapshots ($RETENTION)"
restic forget $RETENTION --prune

# Sample integrity check (full check is slow; 10% subset catches most issues)
echofunc "Verifying repository integrity"
restic check --read-data-subset=10%

echofunc "Done. Latest snapshots:"
restic snapshots --latest 3
