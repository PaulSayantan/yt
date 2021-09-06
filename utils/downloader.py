#!/usr/bin/env python
# -*- coding: utf-8 -*-

from youtube_dl import YoutubeDL
from tqdm import tqdm
from youtube_dl.utils import DownloadError


class Video(object):

    def __init__(self, video: str):
        self.ytdl_opts = {
            'outtmpl': r'%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'verbose': False,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True
        }
        self.__video = video
        self.__video_formats = {}
        self.__audio_formats = {}
        self.title = ''
        self.__pbar = None

    @property
    def video_url(self):
        return self.__video

    @video_url.setter
    def video_url(self, url):
        self.__video = url

    def get_formats(self):
        """function to get all available audio/video formats for a given video
        """

        with YoutubeDL(self.ytdl_opts) as yt:
            data = yt.extract_info(self.__video, download=False)
            self.title = data.get('title', None)
            formats = data.get('formats', [data])
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
        """based on available resolutions, choose the desired and return video id
           by default highest resolution will be choosen

        Returns:
            str: id of the corresponding resolution chosen by user
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

    def get_audio_format(self) -> str:
        """return the audio format with the highest abr value

        Returns:
            tuple[str, str]: audio format and format filesize
        """
        sorted(self.__audio_formats)
        _, vals = self.__audio_formats.popitem()
        return vals['format_id']

    def video_hook(self, downloader):
        """function to display progress status

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

    def download_video(self, path: str):
        """downloading the video

        Args:
            path (str): path where the video will be saved
        """

        self.ytdl_opts['format'] = self.get_video_format() + '+' + self.get_audio_format()
        self.ytdl_opts['progress_hooks'] = [self.video_hook]
        self.ytdl_opts['outtmpl'] = path + self.ytdl_opts['outtmpl']

        try:
            print('Downloading: ', self.title)
            self.__pbar = tqdm(total=100, unit='mb')
            with YoutubeDL(self.ytdl_opts) as dl:
                dl.download([self.__video])
            self.__pbar.close()
        except Exception:
            print('Error in Downloading...')
            raise DownloadError
        print('Download complete')
