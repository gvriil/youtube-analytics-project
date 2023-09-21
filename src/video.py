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
        likes (int): Количество лайков видео.
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
        self.likes = 0

        if not api_key:
            print("Не установлен ключ API YouTube.")
            return

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
        url = f"https://www.googleapis.com/youtube/v3/videos?key={api_key}&id={self.video_id}&part=snippet,statistics"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            video_data = data.get("items")[0]

            self.title = video_data['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.views = int(video_data['statistics']['viewCount'])
            self.likes = int(video_data['statistics']['likeCount'])
        else:
            print("Ошибка при получении данных о видео.")


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


if __name__ == '__main__':
    video = Video('AWX4JnAnjBE')
    assert str(video) == 'GIL в Python: зачем он нужен и как с этим жить'

    pl_video = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
    assert str(pl_video) == 'MoscowPython Meetup 78 - вступление'
