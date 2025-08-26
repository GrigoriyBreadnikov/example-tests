import string
from typing import Dict
from smoke.api.main import GeneralFunctions

#ФАБРИКА ДАННЫХ ДЛЯ ВЕКТОРА


# Инициализация клиентов
GF: GeneralFunctions = GeneralFunctions()
# Константы для валидных и невалидных длин полей
NAME_VALID_LENGTH: Dict[str, int] = {
    "min": 1,  # Минимальная валидная длина имени
    "max": 100,  # Максимальная валидная длина имени
    "start": 2,  # Начало диапазона нормальной длины
    "end": 99  # Конец диапазона нормальной длины
}

# Валидационные константы для тестирования граничных значений полей

NAME_INVALID_LENGTH: Dict[str, int] = {
    "null": 0,      # Нулевая длина (невалидная)
    "start": 101,   # Начало невалидного диапазона (мин. невалидное значение)
    "end": 10000    # Конец невалидного диапазона (макс. невалидное значение)
}

DESCRIPTION_VALID_LENGTH: Dict[str, int] = {
    "min": 1,       # Минимальная валидная длина
    "max": 500,     # Максимальная валидная длина
    "start": 2,     # Начало валидного диапазона
    "end": 499      # Конец валидного диапазона
}

DESCRIPTION_INVALID_LENGTH: Dict[str, int] = {
    "null": 0,      # Нулевая длина (невалидная)
    "start": 501,   # Начало невалидного диапазона
    "end": 1000     # Конец невалидного диапазона
}

CONTENT_VALID_LENGTH: Dict[str, int] = {
    "min": 1,       # Минимальная валидная длина контента
    "max": 500,     # Максимальная валидная длина контента
    "start": 2,     # Начало валидного диапазона
    "end": 499      # Конец валидного диапазона
}

CONTENT_INVALID_LENGTH: Dict[str, int] = {
    "null": 0,      # Нулевая длина (невалидная)
    "start": 501,   # Начало невалидного диапазона
    "end": 1000     # Конец невалидного диапазона
}

LIMIT_VALID_LENGTH: Dict[str, int] = {
    "min": 1,       # Минимальное валидное значение limit
    "max": 100,     # Максимальное валидное значение limit
    "start": 2,     # Начало валидного диапазона
    "end": 99       # Конец валидного диапазона
}

LIMIT_INVALID_LENGTH: Dict[str, int] = {
    "null": 0,      # Нулевое значение (невалидное)
    "start": 101,   # Начало невалидного диапазона
    "end": 1000     # Конец невалидного диапазона
}

PAGE_VALID_LENGTH: Dict[str, int] = {
    "min": 1,       # Минимальное валидное значение page
    "max": 100      # Максимальное валидное значение page
}

PAGE_INVALID_LENGTH: Dict[str, int] = {
    "null": 0       # Нулевое значение (невалидное)
}

# Наборы символов для валидации
NAME_VALID_SYMBOLS: str = f"{string.ascii_letters}._-0123456789"  # Допустимые символы для имени
NAME_INVALID_SYMBOLS: str = f"{GF.get_random_punctuation('[._-]')}{GF.get_russian_letters()}"  # Недопустимые символы для имени
DESCRIPTION_VALID_SYMBOLS: str = f"{GF.get_random_string(string.ascii_letters)}{string.punctuation}0123456789{GF.get_russian_letters()}"  # Допустимые символы для описания

# Константы для пустых значений
NULL: str = ""          # Пустая строка
NULL_SPACE: str = " "   # Строка с пробелом


class VectorRandom:
    """
    Базовый класс для генерации случайных данных векторов.
    Содержит основные методы генерации длины и символов.
    """

    @staticmethod
    def generate_length_vector(min_length: int, max_length: int) -> int:
        """
        Генерирует случайное число в заданном диапазоне.

        Args:
            min_length: Минимальное значение
            max_length: Максимальное значение

        Returns:
            Случайное целое число в диапазоне [min_length, max_length]
        """
        return GF.get_random_int(min_length, max_length)

    @staticmethod
    def generate_symbols_vector(symbols: str) -> str:
        """
        Генерирует случайный символ из заданного набора.

        Args:
            symbols: Строка с допустимыми символами

        Returns:
            Случайный символ из набора symbols
        """
        return GF.get_random_string(symbols)

    @staticmethod
    def generate_full_vector(symbols: str, length: int) -> str:
        """
        Генерирует случайную строку заданной длины из указанных символов.

        Args:
            symbols: Набор допустимых символов
            length: Длина генерируемой строки

        Returns:
            Случайная строка заданной длины
        """
        return GF.make_random_value(symbols, length)


class VectorLength(VectorRandom):
    """
    Класс для генерации тестовых данных с различной длиной полей вектора.
    Наследует базовые методы генерации от VectorRandom.
    """

    def null_name_vector(self) -> int:
        """Возвращает нулевую длину для имени (невалидное значение)"""
        return self.generate_length_vector(NAME_INVALID_LENGTH["null"], NAME_INVALID_LENGTH["null"])

    def min_name_vector(self) -> int:
        """Возвращает минимальную валидную длину для имени"""
        return self.generate_length_vector(NAME_VALID_LENGTH["min"], NAME_VALID_LENGTH["min"])

    def max_name_vector(self) -> int:
        """Возвращает максимальную валидную длину для имени"""
        return self.generate_length_vector(NAME_VALID_LENGTH["max"], NAME_VALID_LENGTH["max"])

    def normal_name_vector(self) -> int:
        """Возвращает нормальную (промежуточную) длину для имени"""
        return self.generate_length_vector(NAME_VALID_LENGTH["start"], NAME_VALID_LENGTH["end"])

    def invalid_name_vector_length(self) -> int:
        """Возвращает невалидную длину для имени (превышающую максимум)"""
        return self.generate_length_vector(NAME_INVALID_LENGTH["start"], NAME_INVALID_LENGTH["end"])

    def null_description_vector(self) -> int:
        """Возвращает нулевую длину для описания (невалидное значение)"""
        return self.generate_length_vector(DESCRIPTION_INVALID_LENGTH["null"], DESCRIPTION_INVALID_LENGTH["null"])

    def min_description_vector(self) -> int:
        """Возвращает минимальную валидную длину для описания"""
        return self.generate_length_vector(DESCRIPTION_VALID_LENGTH["min"], DESCRIPTION_VALID_LENGTH["min"])

    def max_description_vector(self) -> int:
        """Возвращает максимальную валидную длину для описания"""
        return self.generate_length_vector(DESCRIPTION_VALID_LENGTH["max"], DESCRIPTION_VALID_LENGTH["max"])

    def normal_description_vector(self) -> int:
        """Возвращает нормальную (промежуточную) длину для описания"""
        return self.generate_length_vector(DESCRIPTION_VALID_LENGTH["start"], DESCRIPTION_VALID_LENGTH["end"])

    def invalid_vector_description_length(self) -> int:
        """Возвращает невалидную длину для описания (превышающую максимум)"""
        return self.generate_length_vector(DESCRIPTION_INVALID_LENGTH["start"], DESCRIPTION_INVALID_LENGTH["end"])

    def null_content_vector(self) -> int:
        """Возвращает нулевую длину для содержимого (невалидное значение)"""
        return self.generate_length_vector(CONTENT_INVALID_LENGTH["null"], CONTENT_INVALID_LENGTH["null"])

    def min_page_vector_length(self) -> int:
        """Возвращает минимальную допустимую длину для page"""
        return self.generate_length_vector(PAGE_VALID_LENGTH["min"], PAGE_VALID_LENGTH["min"])

    def normal_page_vector_length(self) -> int:
        """Возвращает среднюю (типичную)  длину для page"""
        return self.generate_length_vector(PAGE_VALID_LENGTH["min"], PAGE_VALID_LENGTH["max"])
    def invalid_page_vector_length(self) -> int:
        """Возвращает недопустимую длину для page (превышает максимальный лимит)"""
        return self.generate_length_vector(PAGE_INVALID_LENGTH["null"], PAGE_INVALID_LENGTH["null"])

    def min_limit_vector_length(self) -> int:
        """Возвращает минимальную допустимую длину для limit"""
        return self.generate_length_vector(LIMIT_VALID_LENGTH["min"], LIMIT_VALID_LENGTH["min"])

    def max_limit_vector_length(self) -> int:
        """Возвращает максимальную допустимую длину для limit"""
        return self.generate_length_vector(LIMIT_VALID_LENGTH["max"], LIMIT_VALID_LENGTH["max"])

    def normal_limit_vector_length(self) -> int:
        """Возвращает среднюю (типичную) длину для limit"""
        return self.generate_length_vector(LIMIT_VALID_LENGTH["min"], LIMIT_VALID_LENGTH["max"])

    def invalid_limit_vector_length(self) -> int:
        """Возвращает недопустимую длину для limit (превышает максимальный лимит)"""
        return self.generate_length_vector(LIMIT_INVALID_LENGTH["null"], LIMIT_INVALID_LENGTH["null"])

    def null_limit_vector_length(self) -> int:
        """Возвращает нулевую длину для limit (недопустимое значение)"""
        return self.generate_length_vector(LIMIT_INVALID_LENGTH["null"], NAME_INVALID_LENGTH["null"])

class VectorSymbols(VectorRandom):
    """
    Класс для генерации тестовых данных с различными символами полей вектора.
    Наследует базовые методы генерации от VectorRandom.
    """

    def valid_name_vector_symbols(self) -> str:
        """Возвращает строку с валидными символами для имени"""
        return self.generate_symbols_vector(NAME_VALID_SYMBOLS)

    def invalid_name_vector_symbols(self) -> str:
        """Возвращает строку с невалидными символами для имени"""
        return self.generate_symbols_vector(NAME_INVALID_SYMBOLS)

    def valid_description_vector_symbols(self) -> str:
        """Возвращает строку с валидными символами для описания"""
        return self.generate_symbols_vector(DESCRIPTION_VALID_SYMBOLS)


class VectorFullData(VectorLength, VectorSymbols):
    """
    Класс для генерации полных тестовых данных вектора.
    Объединяет функциональность генерации длины и символов.
    """

    def valid_name_any_length(self, length: int) -> str:
        """
        Генерирует валидное имя вектора заданной длины.

        Args:
            length: Желаемая длина имени

        Returns:
            Строка с валидным именем заданной длины
        """
        return self.generate_full_vector(self.valid_name_vector_symbols(), length)

    def valid_description_any_length(self, length: int) -> str:
        """
        Генерирует валидное описание вектора заданной длины.

        Args:
            length: Желаемая длина описания

        Returns:
            Строка с валидным описанием заданной длины
        """
        return self.generate_full_vector(self.valid_description_vector_symbols(), length)

    def valid_content_any_length(self, length: int) -> str:
        """
        Генерирует валидное содержимое вектора заданной длины.

        Args:
            length: Желаемая длина содержимого

        Returns:
            Строка с валидным содержимым заданной длины
        """
        return self.generate_full_vector(self.valid_name_vector_symbols(), length)

    def name_any_symbols(self, symbols: str) -> str:
        """
        Генерирует имя вектора из заданных символов минимальной длины.

        Args:
            symbols: Набор символов для генерации имени

        Returns:
            Строка с именем из заданных символов
        """
        return self.generate_full_vector(symbols, self.min_name_vector())

    def description_any_symbols(self, symbols: str) -> str:
        """
        Генерирует описание вектора из заданных символов максимальной длины.

        Args:
            symbols: Набор символов для генерации описания

        Returns:
            Строка с описанием из заданных символов
        """
        return self.generate_full_vector(symbols, self.max_description_vector())

    def full_min_name_vector(self) -> str:
        """Генерирует имя с минимальной валидной длиной"""
        return self.valid_name_any_length(self.min_name_vector())

    def full_max_name_vector(self) -> str:
        """Генерирует имя с максимальной валидной длиной"""
        return self.valid_name_any_length(self.max_name_vector())

    def full_normal_name_vector(self) -> str:
        """Генерирует имя с нормальной (промежуточной) длиной"""
        return self.valid_name_any_length(self.normal_name_vector())

    def full_null_name_vector(self) -> str:
        """Генерирует пустое имя (нулевой длины)"""
        return self.valid_name_any_length(self.null_name_vector())

    def full_null_content_vector(self) -> str:
        """Генерирует пустое содержимое (нулевой длины)"""
        return self.valid_content_any_length(self.null_content_vector())

    def full_invalid_name_vector_length(self) -> str:
        """Генерирует имя с невалидной длиной (превышающей максимум)"""
        return self.valid_name_any_length(self.invalid_name_vector_length())

    def full_min_description_vector(self) -> str:
        """Генерирует описание с минимальной валидной длиной"""
        return self.valid_description_any_length(self.min_description_vector())

    def full_max_description_vector(self) -> str:
        """Генерирует описание с максимальной валидной длиной"""
        return self.valid_description_any_length(self.max_description_vector())

    def full_normal_description_vector(self) -> str:
        """Генерирует описание с нормальной (промежуточной) длиной"""
        return self.valid_description_any_length(self.normal_description_vector())

    def full_null_description_vector(self) -> str:
        """Генерирует пустое описание (нулевой длины)"""
        return self.valid_description_any_length(self.null_description_vector())

    def full_invalid_description_vector_length(self) -> str:
        """Генерирует описание с невалидной длиной (превышающей максимум)"""
        return self.valid_description_any_length(self.invalid_vector_description_length())

    def full_vector_content(self) -> str:
        """
        Возвращает фиксированное валидное содержимое вектора.

        Returns:
            Строка с валидным содержимым вектора в YAML-формате
        """
        content = """sources:
  application_logs:
    type: file
    include:
      - /var/log/application.log
    read_from: beginning
transforms:
  final_add_hostname:
    type: remap
    inputs:
      - application_logs
    source: |-
      .hostname = \"${HOSTNAME}\"
      . = ."""
        return content

    def invalid_name_symbols(self) -> str:
        """Генерирует имя с невалидными символами"""
        return self.name_any_symbols(NAME_INVALID_SYMBOLS)

    def space_name_symbols(self) -> str:
        """Генерирует имя, состоящее только из пробелов"""
        return self.name_any_symbols(NULL_SPACE)

    def space_description_symbols(self) -> str:
        """Генерирует описание, состоящее только из пробелов"""
        return self.name_any_symbols(NULL_SPACE)


