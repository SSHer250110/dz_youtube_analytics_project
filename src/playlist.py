import json
import os

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
        :param title: название плейлиста.
        :param url: ссылка на плейлист.
        """
        self.id_playlist = id_playlist
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.id_playlist,
                                                                 part="contentDetails, id, snippet, status",
                                                                 maxResults=50,
                                                                 ).execute()
        self.title = self.playlist_videos["items"][0]["snippet"]["title"][:24]
        self.url = "https://www.youtube.com/playlist?list=" + self.id_playlist

    def total_duration(self):
        """
        Метод возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        (обращение как к свойству, использовать @property)
        """
        pass

    def show_best_video(self):
        """
        Метод возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        pass


playlist = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
# print(playlist.title)
# print(playlist.url)
# print(playlist.playlist_videos)
# with open("playlist.json", "w") as file:
#     json.dump(playlist.playlist_videos, file, ensure_ascii=False)

# api_key = os.getenv("YT_API_KEY")
# youtube = build('youtube', 'v3', developerKey=api_key)

# получить данные по play-листам канала
# playlist = youtube.playlists().list(channelId='UC-OVMPlMA3-YCIeg4z5z23A', part='contentDetails,snippet',
#                                     maxResults=50).execute()
# # print(playlist)
# with open("playlists_channel.json", "w") as f:
#     json.dump(playlist, f, ensure_ascii=False)

# получить данные по видеороликам в плейлисте
# playlist_videos = youtube.playlistItems().list(playlistId="PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw",
#                                                part='contentDetails,snippet',
#                                                maxResults=50,
#                                                ).execute()
# video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
# print(video_ids)
# with open("playlists_items_one.json", "w") as file:
#     json.dump(playlist_videos, file, ensure_ascii=False)
# with open("video_ids.json", "w") as file:
#     json.dump(video_ids, file, ensure_ascii=False)

# вывести длительности видеороликов из плейлиста
# video_response = youtube.videos().list(part='contentDetails,statistics',
#                                        id=','.join(video_ids)
#                                        ).execute()
# print(video_response)
# for video in video_response['items']:
#     # YouTube video duration is in ISO 8601 format
#     iso_8601_duration = video['contentDetails']['duration']
#     duration = isodate.parse_duration(iso_8601_duration)
#     print(duration)
# with open("playlists_video_response.json", "w") as f:
#     json.dump(video_response, f, ensure_ascii=False)
