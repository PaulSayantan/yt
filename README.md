<h1 align="center">yt</h1>

An easy to use YouTube Downloader for downloading YouTube content as video or audio. Written in Python

## Requirements

 * Python 3.7+

## Install
 * Clone / [Download](https://github.com/PaulSayantan/yt/archive/refs/heads/main.zip) the repo

 * Run the command below:
    ```
    cd ./yt
    pip3 install -e .
    ```

## Usage
```
Usage: yt [OPTIONS]

Options:
  -m, --music TEXT                download YouTube video in mp3
  -v, --video TEXT                download YouTube video
  -pl, --playlist <TEXT TEXT>...  download all YouTube videos in a playlist,
                                  denote -a for audio
  -p, --path PATH                 paste the directory where you want to save
                                  the downloaded files, if no path provided,
                                  files will be downloaded in current
                                  directory
  --help                          Show this message and exit.
```

## Note:
Currently, all videos will be downloaded at 1080p as default, if not available, will be downloaded 720p/480p/360p/240p
