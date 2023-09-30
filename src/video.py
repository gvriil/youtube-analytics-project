import os
import requests

# Получаем ключ API YouTube из переменных окружения
api_key = os.getenv("YOUTUBE_API_KEY")


class Video:
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
        self.title = None
        self.url = None
        self.views = None
        self.like_count = None

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
        try:
            # Попытка получить данные о видео по API
            response = requests.get(f'https://api.example.com/video/{self.video_id}')
            data = response.json()
            if 'title' in data and 'likes_count' in data:
                self.title = data['title']
                self.like_count = data['likes_count']
            else:
                self.title = None
                self.like_count = None
        except requests.exceptions.RequestException:
            # Обработка ошибок при запросе к API
            self.title = None
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
