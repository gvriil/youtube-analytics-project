import json
import os

import requests
from googleapiclient.discovery import build

# Получаем ключ API YouTube из переменных окружения
api_key = os.getenv("YOUTUBE_API_KEY")


class Channel:
    """
    Класс для работы с данными о канале YouTube.
    """

    def __init__(self, channel_id):
        """
        Инициализация объекта класса Channel.

        :param channel_id: Идентификатор канала YouTube.
        """
        self.__channel_id = channel_id

        if not api_key:
            print("Не установлен ключ API YouTube.")
            return

        self.title = ""
        self.description = ""
        self.url = ""
        self.subscribers = 0
        self.video_count = 0
        self.view_count = 0

        self.get_info()

    def __str__(self):
        """
        Магический метод __str__, возвращающий название и ссылку на канал по шаблону <название_канала> (<ссылка_на_канал>).
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """
        Магический метод __add__, выполняющий сложение двух каналов по количеству подписчиков.
        """
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        """
        Магический метод __sub__, выполняющий вычитание одного канала из другого по количеству подписчиков.
        """
        return self.subscribers - other.subscribers

    def __eq__(self, other):
        """
        Магический метод __eq__, сравнивающий два канала по количеству подписчиков.
        """
        return self.subscribers == other.subscribers

    def __lt__(self, other):
        """
        Магический метод __lt__, проверяющий, что количество подписчиков у текущего канала меньше, чем у другого канала.
        """
        return self.subscribers < other.subscribers

    def __le__(self, other):
        """
        Магический метод __le__, проверяющий, что количество подписчиков у текущего канала меньше либо равно, чем у другого канала.
        """
        return self.subscribers <= other.subscribers

    @property
    def channel_id(self):
        """
        Получить идентификатор канала.

        :return: Идентификатор канала.
        """
        return self.__channel_id

    def get_info(self):
        """
        Получает информацию о канале из YouTube API и обновляет атрибуты объекта.
        """
        url = f"https://www.googleapis.com/youtube/v3/channels?key={api_key}&id={self.channel_id}&part=snippet,statistics"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            channel_data = data.get("items")[0]

            self.title = channel_data['snippet']['title']
            self.description = channel_data['snippet']['description']
            self.url = f"https://www.youtube.com/channel/{self.channel_id}"
            self.subscribers = int(channel_data['statistics']['subscriberCount'])
            self.video_count = int(channel_data['statistics']['videoCount'])
            self.view_count = int(channel_data['statistics']['viewCount'])
        else:
            print("Ошибка при получении данных о канале.")

    @classmethod
    def get_service(cls):
        """
        Создает и возвращает сервис YouTube API.

        :return: Объект сервиса YouTube API.
        """
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file_name):
        """
        Сохраняет информацию о канале в JSON файл.

        :param file_name: Имя файла для сохранения данных.
        """
        channel_info = {
            "id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "video_count": self.video_count,
            "view_count": self.view_count
        }

        with open(file_name, "w") as json_file:
            json_file.write(json.dumps(channel_info, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    # Пример использования класса Channel
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')

    # Получаем значения атрибутов и выводим их
    print(moscowpython.title)  # MoscowPython
    print(moscowpython.video_count)  # 707 (может уже больше)
    print(moscowpython.url)  # https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A

    # Создаем файл 'moscowpython.json' с данными по каналу
    moscowpython.to_json('moscowpython.json')
