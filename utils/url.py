#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional

from utils.downloader import Playlist


class URLError(Exception):
    def __init__(self, message: str = 'YouTube URL provided is not valid'):
        if message:
            self.message: str = message
        else:
            self.message = None


    def __str__(self):
        if self.message:
            return f'URLError :: {self.message}'
        else:
            return f'URLError occurred'




def valid_url(url: str) -> Optional[str]:
    """ function to check whether link is valid or not
        if valid, return the proper url part, (remove playlist id, if exists)
        if not valid, raise URLError

    Args:
        url (str): url provided by user

    Returns:
        str: YouTube url
    """

    try:
        if url.startswith("https://www.youtube.com/watch?v"):
            if url.find("&list=") != -1:
                return url.split("&list")[0]
            else:
                if len(url.split('?v=')[1]) == 11:
                    return url
                else:
                    raise URLError

        elif url.startswith("https://www.youtube.com/playlist?list="):
            print('This is an Playlist')
            pl = Playlist()
            pl.url = url
            for title, link in pl.playlist_urls():
                print(f'{title}\n')
                print(f'{link}\n--------\n')
            print('pick any of the links you want to download an ')
        else:
            raise URLError
    except URLError as err:
        print(err.message)




def valid_playlist(url: str) -> Optional[str]:
    try:
        if url.startswith("https://www.youtube.com/playlist?list=") and len(url.split('&list=')[1]) == 34:
            return url
        else:
            raise URLError('YouTube URL provided is not a valid playlist')
    except URLError as err:
        print(err.message)
