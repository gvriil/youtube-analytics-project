import json

import isodate

from src.api_key import BaseApi


class Video(BaseApi):
    """
    Класс для работы с данными о видео на YouTube.

    Attributes:
        video_id (str): Идентификатор видео на YouTube.
        title (str): Название видео.
        url (str): Ссылка на видео.
        views (int): Количество просмотров видео.
        like_count (int): Количество лайков видео.
    """

    def __init__(self, video_id):
        """
        Инициализация объекта класса Video.

        Args:
            video_id (str): Идентификатор видео на YouTube.
        """
        self.video_id = video_id
        self.title = ""
        self.url = ""
        self.views = 0
        self.like_count = 0
        self.duration = None
        # if not api_key:
        #     print("Не установлен ключ API YouTube.")
        #     raise

        self.get_video_info()

    def __str__(self):
        """
        Магический метод __str__, возвращающий название видео.

        Returns:
            str: Название видео.
        """
        return f"{self.title}"

    def get_video_info(self):
        """
        Получает информацию о видео из YouTube API и обновляет атрибуты объекта.
        """
        youtube = self.get_service()

        try:
            # Попытка получить данные о видео по API
            response = youtube.videos().list(id=self.video_id,
                                             part='snippet,statistics,contentDetails').execute()
            video_data = response.get("items")[0]

            self.title = video_data['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.views = int(video_data['statistics']['viewCount'])
            self.like_count = int(video_data['statistics']['likeCount'])

            self.duration = isodate.parse_duration(video_data['contentDetails']['duration'])
        except IndexError:
            # Обработка ошибок при запросе к API
            self.title = None
            self.url = None
            self.views = None
            self.like_count = None


class PLVideo(Video):
    """
    Класс для работы с данными о видео в плейлисте на YouTube.
    """

    def __init__(self, video_id, playlist_id):
        """
        Инициализация объекта класса PLVideo.

        Args:
            video_id (str): Идентификатор видео на YouTube.
            playlist_id (str): Идентификатор плейлиста на YouTube.
        """
        self.__playlist_id = playlist_id
        super().__init__(video_id)

    @property
    def playlist_id(self):
        """
        Получить идентификатор плейлиста.

        Returns:
            str: Идентификатор плейлиста.
        """
        return self.__playlist_id
