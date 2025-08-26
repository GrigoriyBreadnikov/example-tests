import random
import string
import re
import datetime
from typing import Set, Union


class GeneralFunctions:
    """
    Класс с общими вспомогательными функциями для генерации тестовых данных.

    Содержит методы для:
    - Генерации случайных чисел
    - Генерации случайных строк
    - Работы со специальными символами
    - Получения русских букв
    - Проверки вхождения элементов
    - Получения текущего времени
    """

    @staticmethod
    def get_random_int(start: int, end: int) -> int:
        """
        Генерирует случайное целое число в заданном диапазоне.

        Args:
            start: Начало диапазона (включительно)
            end: Конец диапазона (включительно)

        Returns:
            Случайное целое число в диапазоне [start, end]
        """
        return random.randint(start, end)

    @staticmethod
    def get_random_string(string: str) -> str:
        """
        Возвращает переданную строку без изменений.

        Args:
            string: Входная строка

        Returns:
            Та же самая строка без изменений
        """
        return string

    @staticmethod
    def get_random_punctuation(punctuation: str) -> str:
        """
        Возвращает все специальные символы, исключая указанные.

        Args:
            punctuation: Строка с символами, которые нужно исключить

        Returns:
            Строка со всеми специальными символами, кроме указанных
        """
        punctuation_all = str(string.punctuation)
        return re.sub(rf"{punctuation}", "", punctuation_all)

    @staticmethod
    def get_russian_letters() -> str:
        """
        Возвращает строку с русскими буквами в обоих регистрах.

        Returns:
            Строка вида "абв...яАБВ...Я" со всеми русскими буквами
        """
        return "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    @staticmethod
    def make_random_value(symbols: str, length: int) -> str:
        """
        Генерирует случайную строку заданной длины из указанных символов.

        Args:
            symbols: Строка с символами, из которых будет генерироваться результат
            length: Длина генерируемой строки

        Returns:
            Случайная строка заданной длины из указанных символов
        """
        value = ''.join(random.choice(symbols) for _ in range(length))
        return value

    @staticmethod
    def now_time() -> str:
        """
        Возвращает текущую дату в формате ISO (без времени).

        Returns:
            Строка с текущей датой в формате "YYYY-MM-DDT"
        """
        date = datetime.date.today()
        now = f"{date}T"
        return now

    @staticmethod
    def contains_all(container: Union[str, Set, list], elements: Union[str, Set, list]) -> bool:
        """
        Проверяет, содержатся ли все элементы из второго аргумента в первом.

        Args:
            container: Контейнер (строка, список, множество), в котором ищем
            elements: Элементы (строка, список, множество), которые ищем

        Returns:
            True если все элементы содержатся в контейнере, иначе False
        """
        return set(elements).issubset(set(container))



