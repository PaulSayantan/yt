#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Dict

from tqdm import tqdm
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError, UnavailableVideoError




class Video:
    """
    Video class to handle downloading of a YouTube video

    """


    def __init__(self):
        self.ytdl_opts = {
            'outtmpl': r'%(title)s.%(ext)s',
            'noplaylist': True,
            'verbose': False,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True
        }
        self.__video: str = ''
        self.__video_formats: dict = {}
        self.__audio_formats: dict = {}
        self.title: str = ''
        self.__pbar: tqdm = None


    @property
    def url(self):
        if self.__video != '':
            return self.__video
        else:
            raise ValueError('URL NOT PROVIDED')


    @url.setter
    def url(self, video):
        if isinstance(video, str):
            self.__video = video
            self.set_formats()
        else:
            raise TypeError


    def set_formats(self):
        """
        function to get all available audio/video formats for a given video

        """

        with YoutubeDL(self.ytdl_opts) as yt:
            data = yt.extract_info(self.__video, download=False)
            self.title = data.get('title', None)
            formats = data.get('formats', None)
        for types in formats:
            info = {}
            if types['format_note'] != 'tiny':
                for k, v in types.items():
                    if k in ['format_id', 'ext']:
                        info[k] = v
                self.__video_formats[int(types['format_note'].split('p')[0])] = info
            else:
                for k, v in types.items():
                    if k in ['format_id', 'ext']:
                        info[k] = v
                self.__audio_formats[int(types['abr'])] = info


    def get_video_format(self, highest=True) -> str:
        """
        1080p resolution will be choosen by default, if not available, choose 720p/480p/360p/240p

        Returns:
            str: video format

        """

        if highest:
            if 1080 in self.__video_formats.keys():
                return self.__video_formats[1080]['format_id']
            elif 720 in self.__video_formats.keys():
                return self.__video_formats[720]['format_id']
            elif 480 in self.__video_formats.keys():
                return self.__video_formats[480]['format_id']
            elif 360 in self.__video_formats.keys():
                return self.__video_formats[360]['format_id']
            elif 240 in self.__video_formats.keys():
                return self.__video_formats[240]['format_id']
        else:
            return 'bestvideo'


    def get_audio_format(self) -> str:
        """return the audio format of the video

        Returns:
            str: audio format
        """
        sorted(self.__audio_formats)
        _, vals = self.__audio_formats.popitem()
        return vals['format_id']


    def video_hook(self, downloader):
        """
        Function to display downloading progress status

        Args:
            downloader: keeps track of the progress of download
        """

        if downloader['status'] == 'downloading':
            percent: str = downloader['_percent_str']
            percent = percent.replace('%', '')
            self.__pbar.n = float(percent)
            self.__pbar.refresh()
        elif downloader['status'] == 'error':
            raise DownloadError


    def dl(self, dir: str = os.getcwd() + '/videos/'):
        """downloading the video

        Args:
            dir (str): dir where the video will be saved
        """

        self.ytdl_opts['format'] = self.get_video_format() + '+' + self.get_audio_format()
        self.ytdl_opts['progress_hooks'] = [self.video_hook]
        self.ytdl_opts['outtmpl'] = dir + self.ytdl_opts['outtmpl']
        self.ytdl_opts['merge_output_format'] = 'mkv'
        try:
            print('Video Downloading: ', self.title)
            self.__pbar = tqdm(total=100, unit='mb', smoothing=0.3)
            with YoutubeDL(self.ytdl_opts) as dl:
                dl.download([self.__video])
            self.__pbar.close()
            self.__pbar = None
        except Exception:
            print('Error in Downloading...')
            raise DownloadError
        print('Download complete')




class Audio:
    """
    Music class to handle downloading of a YouTube audio

    """


    def __init__(self):
        self.ytdl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': r'%(title)s.%(ext)s',
            'merge_output_format': 'mp3',
            'noplaylist': True,
            'verbose': False,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        self.__audio: str = ''
        self.__pbar: tqdm = None


    @property
    def url(self):
        if self.__audio != '':
            return self.__audio
        else:
            raise ValueError('URL NOT PROVIDED')


    @url.setter
    def url(self, audio: str):
        if isinstance(audio, str):
            self.__audio = audio
        else:
            raise TypeError


    def title(self):
        """
        Function to retrieve Title of audio

        Returns:
            str: title

        """

        with YoutubeDL(self.ytdl_opts) as yt:
            data = yt.extract_info(self.__audio, download=False)
            return data.get('title', None)


    def audio_hook(self, downloader):
        """
        Function to display progress status

        Args:
            downloader: keeps track of the progress of download

        """

        if downloader['status'] == 'downloading':
            percent: str = downloader['_percent_str']
            percent = percent.replace('%', '')
            self.__pbar.n = float(percent)
            self.__pbar.refresh()
        elif downloader['status'] == 'error':
            raise DownloadError


    def dl(self, dir: str = os.getcwd() + '/audios/'):
        """downloading the audio

        Args:
            dir: directory where the music/audio file will be saved

        """

        self.ytdl_opts['progress_hooks'] = [self.audio_hook]
        self.ytdl_opts['outtmpl'] = dir + self.ytdl_opts['outtmpl']
        print('Audio Downloading: ', self.title())
        self.__pbar = tqdm(total=100, unit='mb', smoothing=0.9)
        try:
            with YoutubeDL(self.ytdl_opts) as yt:
                yt.download([self.__audio])
            self.__pbar.close()
            self.__pbar = None
        except Exception:
            print('Error in Downloading')
            raise DownloadError
        print('Download complete')




class Playlist:
    """
    Playlist class to handle downloading all YouTube videos/audios from the given playlist

    """


    def __init__(self):
        self.ytdl_opts = {
            'outtmpl': r'%(id)s-%(title)s.%(ext)s',
            'quiet': True
        }
        self.__playlist: str = ''
        self.__name: str = ''


    @property
    def url(self):
        if self.__playlist != '':
            return self.__playlist
        else:
            raise ValueError('URL NOT PROVIDED')


    @url.setter
    def url(self, playlist):
        if isinstance(playlist, str):
            self.__playlist = playlist
        else:
            raise TypeError


    def playlist_urls(self) -> Dict[str, str]:
        """
        Retrieve all the video urls from the playlist
        Returns:
            List[str]: list of all the videos in the playlist
        """

        urls = {}
        try:
            print('Retrieving URLs from the playlist....')
            with YoutubeDL(self.ytdl_opts) as yt:
                data = yt.extract_info(self.__playlist, download=False)
                if 'entries' in data:
                    playlist = data['entries']
                    print('Playlist :: ', playlist[0]['playlist'])
                    self.__name = playlist[0]['playlist']
                    for item in playlist:
                        urls[item['title']] = item['webpage_url']
                else:
                    print('This is not an YouTube Playlist URL')
        except Exception:
            raise UnavailableVideoError
        finally:
            return urls


    def dl(self, dtype: str, dir: str = os.getcwd() + '/Playlists/'):
        """
        Download all videos/audios of the playlist
        Args:
            dir: directory where the videos/audio will be saved
            dtype: whether all urls will be downloaded as videos or audios
            urls: list of all urls in the playlist

        """

        urls = self.playlist_urls()

        __dir = dir + self.__name
        if dtype == 'audio':
            for _, link in urls.items():
                audio = Audio()
                audio.url = link
                audio.dl(dir=__dir)
        elif dtype == 'video':
            for _, link in urls.items():
                video = Video()
                video.url = link
                video.dl(dir=__dir)
