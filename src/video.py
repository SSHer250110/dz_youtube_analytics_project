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
        :param name_video: Название видео.
        :param url_video: Ссылка на видео.
        :param number_of_views: Количество просмотров.
        :param number_of_likes: Количество лайков.
        """
        self.id_video = id_video
        self.name_video = self.get_info_video()["items"][0]["snippet"]["title"]
        self.url_video = "https://www.youtube.com/watch?v=" + self.id_video
        self.number_of_views = self.get_info_video()["items"][0]["statistics"]["viewCount"]
        self.number_of_likes = self.get_info_video()["items"][0]["statistics"]["likeCount"]

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
        return self.name_video


class PLVideo(Video):
    """
    Класс со свойствами и методами плейлиста
    """

    def __init__(self, id_video, id_playlist):
        """
        Создание экземпляра класса plvideo.

        :param id_video: id видео.
        :param id_playlist: id плейлиста.
        :param name_video: Название видео.
        :param url_video: Ссылка на видео.
        :param number_of_views: Количество просмотров.
        :param number_of_likes: Количество лайков.
        """
        super().__init__(id_video)
        self.id_playlist = id_playlist
        self.name_video = self.get_info_video()["items"][0]["snippet"]["title"]
        self.url_video = "https://www.youtube.com/watch?v=" + self.id_video
        self.number_of_views = self.get_info_video()["items"][0]["statistics"]["viewCount"]
        self.number_of_likes = self.get_info_video()["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        """
        Метод для отображения информации для пользователя.
        """
        return self.name_video
