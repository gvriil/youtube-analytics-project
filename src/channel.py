# print(os.getenv("YOUTUBE_API_KEY"))
#
# # src/channel.py
import os
import requests

class Channel:
    """
    Класс для работы с YouTube каналом.

    Args:
        channel_id (str): ID YouTube канала.

    Attributes:
        channel_id (str): ID YouTube канала.
        api_key (str): Ключ API для доступа к YouTube Data API.

    Methods:
        print_info(): Получает и выводит информацию о канале.

    Examples:
        Создание объекта канала и получение информации о нем:
        >>> moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
        >>> moscowpython.print_info()
    """
    def __init__(self, channel_id):
        """
        Инициализирует объект канала с заданным ID.

        Args:
            channel_id (str): ID YouTube канала.
        """
        self.channel_id = channel_id
        self.api_key = os.getenv("YOUTUBE_API_KEY")

    def print_info(self):
        """
       Получает и выводит информацию о канале, включая ID.

       Returns:
           None
        """
        if not self.api_key:
            print("Не установлен ключ API YouTube.")
            return

        url = f"https://www.googleapis.com/youtube/v3/channels?key={self.api_key}&id={self.channel_id}&part=snippet,statistics"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            channel_data = data.get("items")[0]

            print(f"Информация о канале: {channel_data['id']}")
            print(f"Название: {channel_data['snippet']['title']}")
            print(f"Описание: {channel_data['snippet']['description']}")
            print(f"Количество подписчиков: {channel_data['statistics']['subscriberCount']}")
            print(f"Количество просмотров: {channel_data['statistics']['viewCount']}")
        else:
            print("Ошибка при получении данных о канале.")
