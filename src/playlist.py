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
        :param info_videos_playlist: данные видеороликов в плейлисте.
        :param title: название плейлиста.
        :param url: ссылка на плейлист.
        :param ids_video: id всех видеороликов плейлиста(список).
        :param info_videos_playlist: информация по видеороликам плейлиста.
        """
        self.id_playlist = id_playlist
        self.info_videos_playlist = self.youtube.playlistItems().list(playlistId=self.id_playlist,
                                                                      part="contentDetails, id, snippet, status",
                                                                      maxResults=50,
                                                                      ).execute()
        self.title = self.info_videos_playlist["items"][0]["snippet"]["title"][:24]
        self.url = "https://www.youtube.com/playlist?list=" + self.id_playlist
        self.ids_video = [video['contentDetails']['videoId'] for video in self.info_videos_playlist['items']]
        self.length_videos_playlist = self.youtube.videos().list(part='contentDetails,statistics',
                                                                 id=','.join(self.ids_video)
                                                                 ).execute()

    @property
    def total_duration(self):
        """
        Метод возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """
        length_videos = timedelta(seconds=0)
        for video in self.length_videos_playlist['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            length_videos += duration
        return length_videos

    def show_best_video(self):
        """
        Метод возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        likes = 0
        video_url = None
        for video in self.length_videos_playlist["items"]:
            if int(video["statistics"]["likeCount"]) > likes:
                video_url = video["id"]
                likes = int(video["statistics"]["likeCount"])
        return f"https://youtu.be/{video_url}"
