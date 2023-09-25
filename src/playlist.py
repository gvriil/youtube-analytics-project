import os
import requests
from datetime import timedelta

# Получаем ключ API YouTube из переменных окружения
api_key = os.getenv("YOUTUBE_API_KEY")


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = ""
        self.url = ""
        self.videos = []

        if not api_key:
            print("Не установлен ключ API YouTube.")
            return

        self.get_playlist_info()

    def get_playlist_info(self):
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
        total_duration_seconds = sum(video.duration.total_seconds() for video in self.videos)
        return timedelta(seconds=total_duration_seconds)

    def show_best_video(self):
        if not self.videos:
            return None
        best_video = max(self.videos, key=lambda video: video.likes)
        return best_video.url


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.title = ""
        self.url = ""
        self.views = 0
        self.likes = 0
        self.duration = timedelta()

        if not api_key:
            print("Не установлен ключ API YouTube.")
            return

        self.get_video_info()

    def get_video_info(self):
        url = f"https://www.googleapis.com/youtube/v3/videos?key={api_key}&id={self.video_id}&part=snippet,statistics,contentDetails"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            video_data = data.get("items")[0]

            self.title = video_data['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.views = int(video_data['statistics']['viewCount'])
            self.likes = int(video_data['statistics']['likeCount'])
            duration = video_data['contentDetails']['duration']
            self.duration = parse_duration(duration)
        else:
            print("Ошибка при получении данных о видео.")


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
