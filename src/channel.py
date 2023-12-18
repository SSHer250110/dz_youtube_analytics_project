import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class Channel:
    """Класс для ютуб-канала"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key = os.getenv("YT_API_KEY")
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]['snippet']['localized']['title']
        self.description = self.channel["items"][0]['snippet']['localized']['description']
        self.url = self.channel["items"][0]['snippet']['customUrl']
        self.count_subscribers = self.channel["items"][0]["statistics"]['subscriberCount']
        self.video_count = self.channel["items"][0]["statistics"]['videoCount']
        self.total_views = self.channel["items"][0]["statistics"]['viewCount']

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Класс-метод, возвращающий объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, file_path):
        """
        Метод, сохраняющий в файл значения атрибутов экземпляра Channel
        """
        data_dict = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "count_subscribers": self.count_subscribers,
            "video_count": self.video_count,
            "total_views": self.total_views
        }

        with open(file_path, "a") as f:
            if os.stat(file_path).st_size == 0:
                json.dump([data_dict], f, ensure_ascii=False)
            else:
                with open(file_path) as f:
                    data_list = json.load(f)
                    data_list.append(data_dict)
                with open(file_path, "w") as f:
                    json.dump(data_list, f, ensure_ascii=False)
