# Batch Rename

## For file-system

<<< @/assets/batch-rename.py

### Usage
```sh
# /videos/TVShow/some-tv/some-tv.s01.e03.1080p.Bluray.mkv -> /videos/TVShow/some-tv/Some.Tv.S01E03.mkv
python batch-rename.py -f "/videos/TVShow/some-tv" -s "^.*?s(\d+)\.e(\d+)\.(.*)$" -d "Some.Tv.S\1E\2\3"
```

## For QBittorent
The `batch_rename` function is the same as the one above.

<<< @/assets/batch-rename-qbt.py

### Usage
```sh
python main.py -u "https://qbt.yunyuyuan.net/" -c "SID=xxxxxxxxxxxxxxx"
```