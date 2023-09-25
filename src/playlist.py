import os
from datetime import timedelta

import requests

from src.video import Video

# Получаем ключ API YouTube из переменных окружения
api_key = os.getenv("YOUTUBE_API_KEY")


class PlayList:
    """
    Класс для работы с данными о плейлисте YouTube.
    """

    def __init__(self, playlist_id):
        """
        Инициализация объекта класса PlayList.

        :param playlist_id: Идентификатор плейлиста YouTube.
        """
        self.playlist_id = playlist_id
        self.title = ""
        self.url = ""
        self.videos = []

        if not api_key:
            print("Не установлен ключ API YouTube.")
            return

        self.get_playlist_info()

    def get_playlist_info(self):
        """
        Получает информацию о плейлисте из YouTube API и обновляет атрибуты объекта.
        """
        url = f"https://www.googleapis.com/youtube/v3/playlists?key={api_key}&id={self.playlist_id}&part=snippet"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            playlist_data = data.get("items")[0]

            self.title = playlist_data['snippet']['title']
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

            # Получение видео из плейлиста
            self.get_playlist_videos()
        else:
            print("Ошибка при получении данных о плейлисте.")

    def get_playlist_videos(self):
        """
        Получает информацию о видео в плейлисте из YouTube API и обновляет список видео в атрибуте объекта.
        """
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?key={api_key}&playlistId={self.playlist_id}&part=snippet"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            video_items = data.get("items")

            for video_item in video_items:
                video_id = video_item['snippet']['resourceId']['videoId']
                video = Video(video_id)
                self.videos.append(video)
        else:
            print("Ошибка при получении видео из плейлиста.")

    @property
    def total_duration(self):
        """
        Возвращает суммарную продолжительность видео в плейлисте в формате timedelta.

        :return: Суммарная продолжительность видео в плейлисте.
        :rtype: timedelta
        """
        total_duration_seconds = sum(video.duration.total_seconds() for video in self.videos)
        return timedelta(seconds=total_duration_seconds)

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео в плейлисте (по количеству лайков).

        :return: Ссылка на самое популярное видео в плейлисте.
        :rtype: str
        """
        if not self.videos:
            return None
        best_video = max(self.videos, key=lambda video: video.likes)

        # Извлечь video_id из полного URL видео
        video_id = best_video.video_id

        # Собрать новый URL в формате "https://youtu.be/{video_id}"
        best_video_url = f"https://youtu.be/{video_id}"

        return best_video_url


def parse_duration(duration_str):
    # Функция для парсинга продолжительности видео в формате PT1H23M45S
    duration_str = duration_str.replace("PT", "")
    hours, minutes, seconds = 0, 0, 0

    if 'H' in duration_str:
        hours, duration_str = duration_str.split('H')
        hours = int(hours)
    if 'M' in duration_str:
        minutes, duration_str = duration_str.split('M')
        minutes = int(minutes)
    if 'S' in duration_str:
        seconds = int(duration_str.replace('S', ''))

    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


# тестируем полученную ссылку
pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
print(f"{pl.show_best_video}")
best_video_url = pl.show_best_video()
print("Best Video URL:", best_video_url)
