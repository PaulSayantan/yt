#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click import STRING, Path, Tuple, command, option

from utils.downloader import Audio, Video  
from utils.url import *


@command()
@option('--music', '-m', type=STRING, help='download YouTube video in mp3')
@option('--video', '-v', type=STRING, help='download YouTube video')
@option('--playlist', '-pl', nargs=2, type=Tuple([STRING, STRING]), help='download all YouTube videos in a playlist, denote a for audio')
@option('--path', '-p', required=False, type=Path(), help='paste the directory where you want to save the downloaded files, if no path provided, files will be downloaded in current directory')
def cli(music, video, playlist, path):
    if music:
        audio = Audio()
        audio.url = valid_url(music)
        if path:
            audio.dl(dir=path)
        else:
            audio.dl()
    elif video:
        vid = Video()
        vid.url = valid_url(video)
        if path:
            vid.dl(dir=path)
        else:
            vid.dl()
    elif playlist:
        pl = Playlist()
        pl.url = valid_playlist(playlist[0])
        
        if playlist[1]:
            dt: str = playlist[1]
        if path:
            if dt == 'a' or dt == 'audio':
                pl.dl(dtype='audio', dir=path)
            else:
                pl.dl(dtype='video', dir=path)
        else:
            if dt == 'a' or dt == 'audio':
                pl.dl(dtype='audio')
            else:
                pl.dl(dtype='video')




if __name__ == '__main__':
    cli()
