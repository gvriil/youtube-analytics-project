"""
Этот скрипт создает экземпляр класса `Channel` и использует его для получения и вывода информации
 о канале YouTube.

Сначала он импортирует класс `Channel` из модуля `src.channel`. Затем, если этот скрипт выполняется
как основная программа (а не импортируется как модуль), он создает экземпляр класса `Channel`,
передавая идентификатор канала YouTube в качестве аргумента. Затем вызывается метод `print_info()`,
который получает информацию о канале и выводит ее на экран.

Примечание: Для успешной работы этого скрипта необходимо установить переменную окружения
`YOUTUBE_API_KEY` с ключом API YouTube.

Пример использования:
    $ python main.py
"""
from src.channel import Channel


def main():
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    moscowpython.print_info()


if __name__ == '__main__':
    main()
