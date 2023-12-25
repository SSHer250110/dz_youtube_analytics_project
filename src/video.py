import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class Video:
    """
    Класс со свойствами и методами одного видео
    """
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key = os.getenv("YT_API_KEY")
    # создать специальный объект для работы с API
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, id_video):
        """
        Создание экземпляра класса video.

        :param id_video: id видео.
        :param title: Название видео.
        :param url_video: Ссылка на видео.
        :param number_of_views: Количество просмотров.
        :param like_count: Количество лайков.
        """
        try:
            self.id_video = id_video
            self.title = self.get_info_video()["items"][0]["snippet"]["title"]
            self.url_video = "https://www.youtube.com/watch?v=" + self.id_video
            self.number_of_views = self.get_info_video()["items"][0]["statistics"]["viewCount"]
            self.like_count = self.get_info_video()["items"][0]["statistics"]["likeCount"]
        except IndexError:
            self.id_video = id_video
            self.title = None
            self.url_video = None
            self.number_of_views = None
            self.like_count = None

    def get_info_video(self):
        """
        Метод получения информации о видео
        """
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.id_video
                                                    ).execute()
        return video_response

    def __str__(self):
        """
        Метод для отображения информации для пользователя.
        """
        return self.title


class PLVideo(Video):
    """
    Класс со свойствами и методами видео плейлиста
    """

    def __init__(self, id_video, id_playlist):
        """
        Создание экземпляра класса plvideo.

        :param id_video: id видео.
        :param id_playlist: id плейлиста.
        :param title: Название видео.
        :param url_video: Ссылка на видео.
        :param number_of_views: Количество просмотров.
        :param like_count: Количество лайков.
        """
        super().__init__(id_video)
        self.id_playlist = id_playlist
        self.title = self.get_info_video()["items"][0]["snippet"]["title"]
        self.url_video = "https://www.youtube.com/watch?v=" + self.id_video
        self.number_of_views = self.get_info_video()["items"][0]["statistics"]["viewCount"]
        self.like_count = self.get_info_video()["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        """
        Метод для отображения информации для пользователя.
        """
        return self.title
