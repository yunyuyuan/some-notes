# Files Backup

Application-level backup for an Arch Linux server using [Restic](https://restic.net/)
with an [rclone](https://rclone.org/) remote backend. Restic gives you
deduplication, encryption, incremental snapshots and — unlike a plain `tar`
archive — a real **restore** workflow.

## Need to backup

* `/etc`
* `/home`
* `/boot`
* `/root`
* `/var/www`
* `/data`
* MariaDB (dumped to a file first — see below)
* optional:
  * `/opt`

::: warning
Never back up a **live** database by copying its data files. Dump it first
(`mariadb-dump`) so the snapshot is consistent, then let Restic pick up the dump.
:::

## Why Restic instead of `tar`

| | `tar.gz` (old) | Restic (new) |
| --- | --- | --- |
| Incremental | ❌ full every time | ✅ only changed chunks |
| Deduplication | ❌ | ✅ content-defined chunking |
| Encryption | ❌ | ✅ AES-256 |
| Restore single file | extract whole archive | `restic restore`/`mount` |
| Versioning / retention | manual file juggling | `forget --keep-*` policy |
| Integrity check | ❌ | `restic check` |

## Prerequisites

```sh
sudo pacman -S restic rclone
```

Configure an rclone remote first (`rclone config`); the script below assumes a
remote named `<your-remote>`.

Create a strong repository password and store it in a file. **Also save this
password somewhere safe (a password manager) — if you lose it, the backups are
unrecoverable.**

```sh
openssl rand -base64 32 > "$HOME/.restic-password"
chmod 600 "$HOME/.restic-password"
```

## The backup script

```sh
vim /home/<user>/my-backup.sh
```

```sh
######
# Change this:
USER=<user>
USER_DIR=/home/$USER
# Restic repository via rclone backend
RESTIC_REPOSITORY=rclone:<your-remote>:/home-arch-backup
# Password file for restic (chmod 600)
RESTIC_PASSWORD_FILE=$USER_DIR/.restic-password
# Local MariaDB dump dir (will be included in the restic snapshot)
DB_DUMP_DIR=/var/backups/mariadb
# Retention policy applied after each backup
RETENTION="--keep-monthly 3"
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
/data/next-cloud/data/**/files_versions
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
```

## crontab task

```sh
sudo crontab -e
```

```sh
# Run at 00:00 on day 5 of every month
0 0 5 * * sh /home/<user>/my-backup.sh >> /var/log/my-backup.log 2>&1
```

::: info
Recommended to use `logrotate` to control the size of the log.
:::

## Restore

List snapshots to find the one you want:

```sh
export RESTIC_REPOSITORY=rclone:<your-remote>:/home-arch-backup
export RESTIC_PASSWORD_FILE=$HOME/.restic-password

restic snapshots
```

Restore an entire snapshot to a staging directory (safer than restoring straight
to `/`):

```sh
restic restore latest --target /restore-tmp
```

Restore only a sub-path:

```sh
restic restore latest --target /restore-tmp --include /etc
```

Browse a snapshot like a normal directory (FUSE mount), copy out what you need:

```sh
mkdir -p /mnt/restic
restic mount /mnt/restic
# ... browse /mnt/restic, then Ctrl-C to unmount
```

Restore the MariaDB dump and load it back:

```sh
restic restore latest --target / --include /var/backups/mariadb
gunzip < /var/backups/mariadb/all-databases_YYYY-MM-DD.sql.gz | mariadb
```

## Removing files you forgot to exclude

If something got backed up that should have been excluded (e.g. you added a new
exclude pattern later), use `restic rewrite` to strip it from **existing**
snapshots, then `prune` to actually reclaim the space.

```sh
# 1. See which snapshots contain the path
restic find "/data/jellyfin/config/data/transcodes"

# 2. Dry-run: preview which snapshots change and how much space is freed
restic rewrite --exclude "/data/jellyfin/config/data/transcodes" --dry-run

# 3. Rewrite all snapshots, dropping the path.
#    --forget removes the pre-rewrite version of each affected snapshot.
restic rewrite --exclude "/data/jellyfin/config/data/transcodes" --forget

# 4. Reclaim storage on the remote (rewrite alone does NOT free space)
restic prune
```

Notes:

* Rewritten snapshots get a **new ID** (their content changed); the old IDs are
  forgotten. Don't hard-code snapshot IDs anywhere.
* `--exclude` can be repeated, or use `--exclude-file=<file>` to clean up many
  paths at once — handy for retroactively applying the full exclude list above.
* By default `rewrite` touches **all** snapshots. Limit the scope with `--host`,
  `--tag` or an explicit snapshot ID.
* `prune` can be slow on large repositories — run it manually rather than from cron.

## Maintenance

```sh
# Full integrity check including all data (slow; run occasionally)
restic check --read-data

# Repository stats / how much space is actually used
restic stats
restic stats --mode raw-data

# Unlock if a previous run was interrupted and left a stale lock
restic unlock
```

## Comparison of application-level backup tools

Restic is not the only option. For reference, the main contenders that work at
the **application layer** (no btrfs/zfs snapshots required):

| Tool | Dedup | Encryption | Backends | UI | Notes |
| --- | --- | --- | --- | --- | --- |
| **Restic** | ✅ | ✅ | S3/B2/Azure/GCS/SFTP/rclone | CLI | Best all-rounder, native rclone |
| **BorgBackup** | ✅ | ✅ | SSH (rclone via wrapper) | CLI (+Borgmatic) | Best compression ratio |
| **Kopia** | ✅ | ✅ | S3/B2/Azure/WebDAV/… | ✅ Web UI | Server mode for multiple machines |
| **Duplicacy** | ✅ | ✅ | most clouds | Web (paid) | Lock-free multi-client dedup |
| **ReaR** | ❌ | ❌ | NFS/USB/CIFS | CLI | Bare-metal recovery (bootable ISO) |

For full bare-metal recovery (re-partition + reinstall onto blank/new hardware),
pair the data backup above with [ReaR (Relax-and-Recover)](https://relax-and-recover.org/).
