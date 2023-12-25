import json
import os
from datetime import timedelta

import isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class PlayList:
    """
    Класс со свойствами и методами плейлиста
    """
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key = os.getenv("YT_API_KEY")
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_playlist):
        """
        Создание экземпляра класса PlayList
        :param id_playlist: id плейлиста.
        :param data_videos_playlist: данные видеороликов в плейлисте.
        :param title: название плейлиста.
        :param url: ссылка на плейлист.
        :param ids_video: id всех видеороликов плейлиста(список).
        :param length_videos_playlist: длительность видеороликов плейлиста.
        """
        self.id_playlist = id_playlist
        self.data_videos_playlist = self.youtube.playlistItems().list(playlistId=self.id_playlist,
                                                                      part="contentDetails, id, snippet, status",
                                                                      maxResults=50,
                                                                      ).execute()
        self.title = self.data_videos_playlist["items"][0]["snippet"]["title"][:24]
        self.url = "https://www.youtube.com/playlist?list=" + self.id_playlist
        self.ids_video: list[str] = [video['contentDetails']['videoId'] for video in self.data_videos_playlist['items']]
        self.length_videos_playlist = self.youtube.videos().list(part='contentDetails,statistics',
                                                                 id=','.join(self.ids_video)
                                                                 ).execute()
