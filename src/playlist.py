from datetime import timedelta
from src.api_key import BaseApi
from src.video import Video


class PlayList(BaseApi):
    """
    Класс для работы с данными о плейлисте YouTube.
    """

    def __init__(self, playlist_id):

        """
        Инициализация объекта класса PlayList.

        :param playlist_id: Идентификатор плейлиста YouTube.
        """
        self._playlist_data = None
        self._playlist_videos_data = None
        self.youtube = self.get_service()
        self.playlist_id = playlist_id
        self.title = ""
        self.url = ""
        self.videos = []
        self.get_playlist_info()

    def get_playlist_info(self):
        """
        Получает информацию о плейлисте из YouTube API и обновляет атрибуты объекта.
        """
        try:
            self._playlist_data = self.youtube.playlists().list(id=self.playlist_id,
                                                                part='snippet').execute()

            playlist_data = self._playlist_data.get("items")[0]

            self.title = playlist_data['snippet']['title']
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

            # Получение видео из плейлиста
            self.get_playlist_videos()
        except IndexError:
            raise Exception('Не удалось получить данные о плейлисте')

    def get_playlist_videos(self):
        """
        Получает информацию о видео в плейлисте из YouTube API и обновляет список видео в атрибуте объекта.
        """

        try:
            self._playlist_videos_data = self.youtube.playlistItems().list(
                playlistId=self.playlist_id, part='snippet').execute()
            video_items = self._playlist_videos_data.get("items")
            for video_item in video_items:
                video_id = video_item['snippet']['resourceId']['videoId']
                video = Video(video_id)
                self.videos.append(video)
        except IndexError:
            raise Exception('Ошибка при получении видео из плейлиста.')

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
        best_video = max(self.videos, key=lambda video: video.like_count)

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
