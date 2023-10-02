import os

from googleapiclient.discovery import build


class BaseApi:
    api_key = os.getenv("YOUTUBE_API_KEY")

    @classmethod
    def get_service(cls):
        """
        Создает и возвращает сервис YouTube API.

        :return: Объект сервиса YouTube API.
        """
        return build('youtube', 'v3', developerKey=cls.api_key)
