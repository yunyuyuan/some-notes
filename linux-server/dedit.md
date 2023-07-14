# Edit docker container files from host

### create `dedit.sh` in host
```sh
#!/bin/bash
IFS=$'\n\t'
set -euox pipefail


CNAME="$1"
FILE_PATH="$2"

FILE_NAME="$(basename "$FILE_PATH")"
TMPFILE="$(mktemp --suffix=_$FILE_NAME)"
docker exec "$CNAME" cat "$FILE_PATH" > "$TMPFILE"
$EDITOR "$TMPFILE"
cat "$TMPFILE" | docker exec -i "$CNAME" sh -c 'cat > '"$FILE_PATH"
rm "$TMPFILE"
```

### Usage
```sh
export EDITOR=vim
sh dedit.sh 70223187131b /app/main.py
```