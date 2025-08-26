import pytest
import allure
import httpx
from allure_commons.types import LabelType, Severity
from smoke.api.vector.tests.faker import VectorFullData, VectorLength
from smoke.api.vector.tests.steps import StepsTestVector

#API-ТЕСТЫ ВЕКТОРА


"""
Константы для организации тестов в Allure Report

Константы для структурирования тестов по иерархии Allure:
- EPIC -> FEATURE -> STORY
- Группировка в test suites
- Маркировка тегов для фильтрации
- Ссылки на внешние ресурсы
"""

# Уровни Allure-иерархии
EPIC: str = "API"                          # Высокоуровневая категория
FEATURE: str = "VECTOR CRUD OPERATIONS"    # Функциональная область
PARENT_SUITE: str = "API"                  # Родительский набор тестов
SUITE: str = "VECTOR API TESTING"          # Специализированный набор тестов

# Теги для категоризации
POSITIVE_TAG: str = "positive"             # Позитивные сценарии
NEGATIVE_TAG: str = "negative"             # Негативные сценарии
DUPLICATE_TAG: str = "duplicate"           # Тесты на дублирование

# Ссылки на внешние ресурсы
TEST_REPO: str = "https://gitlab.158-160-60-159.sslip.io/astra-monitoring-icl/testing/astra-monitoring-tests"
SWAGGER: str = "https://gitlab.158-160-60-159.sslip.io/astra-monitoring-icl/admin-backend/-/blob/dev/docs/swagger.json?ref_type=heads"

""""
Модуль тестирования функционала векторов API

Содержит комплекс тестов для проверки:
- Метода Post
- Метода Patch
- Метода Get
- Метода Delete
"""

# Инициализация вспомогательных классов для тестирования векторов

step = StepsTestVector()        # Класс с шагами тестирования (API-запросы и проверки)
data = VectorFullData()         # Класс с тестовыми данными (валидные/невалидные значения полей)
data_len = VectorLength()       # Класс с параметрами длины для валидации (граничные значения)


@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("POST VECTOR")
@allure.parent_suite(PARENT_SUITE)
@allure.suite(SUITE)
@allure.tag("api", "rest", "vector", "create")
@allure.label(LabelType.LANGUAGE, "python")
@allure.label(LabelType.FRAMEWORK, "pytest")
@allure.link(
   TEST_REPO,
    name="Ссылка на репозиторий с тестами",
)
@allure.link(
   SWAGGER, name="Ссылка на swagger с методами для Vector"
)
@pytest.mark.usefixtures("get_token")
@pytest.mark.flaky(reruns=10, reruns_delay=1, rerun_exceptions=httpx.ConnectError)
class TestPostVector:
    """
    Класс тестов для проверки создания векторов через POST-запросы

    Использует фикстуру get_token для получения JWT токена авторизации
    перед выполнением каждого теста.

    Содержит тесты:
    - С корректными данными (минимальные, максимальные, нормальные значения)
    - С некорректными данными (null, недопустимая длина, спецсимволы)
    - Граничные случаи (пропуск обязательных полей, пробелы, дубликаты)
    """

    # --------------------------------------------------
    # Тесты с валидными данными
    # --------------------------------------------------

    @allure.title("Тест создания вектора с минимально допустимыми значениями полей")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(POSITIVE_TAG)
    @pytest.mark.flaky(reruns=10, reruns_delay=1, rerun_exceptions=httpx.ConnectError)
    def test_create_min_vector(self):
        """
        POSITIVE TEST. BLOCKER severity.
        Проверяет создание вектора с минимально допустимыми значениями полей.

        Тест критически важен для обеспечения базовой функциональности системы.

        Что проверяет:
        - Запрос возвращает статус 201 (Created)
        - В ответе генерируется корректный ID объекта
        - Все переданные значения (name, description, content)
          возвращаются в ответе без изменений

        Особенности:
        - Использует минимальные валидные значения для всех полей
        - Тест самоочищается (удаляет созданный вектор после проверок)
        - Настроены повторные запуски при падении (10 попыток с задержкой 1 сек)
          для обработки временных нестабильностей окружения

        Expected: Вектор должен быть успешно создан со всеми переданными данными.
        """

        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора с минимальными валидными значениями
        vector_data = step.data_prepare_full(data.full_min_name_vector(), data.full_min_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора
        response = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (201 Created)
        step.check_status_201(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID созданного вектора корректной длины
        step.check_response_id_len(response)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_post_response_name(response, vector_data["name"])

        # 3.4 ПРОВЕРКА: Описание вектора в ответе соответствует переданному значению
        step.check_post_response_description(response, vector_data["description"])

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_post_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: Время создания вектора соответствует текущему времени (с допустимой погрешностью)
        step.check_response_created_time(response)

        # 4. ОЧИСТКА ОКРУЖЕНИЯ: Удаление созданного вектора
        step.clean_env(self.token, response)

    @allure.title("Тест создания вектора с максимально допустимыми значениями полей")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(POSITIVE_TAG)
    def test_create_max_vector(self):
        """
        POSITIVE TEST. BLOCKER severity.
        Проверяет создание вектора с максимально допустимыми значениями полей.

        Тест критически важен для проверки верхних границ допустимых значений.

        Что проверяет:
        - Система корректно обрабатывает поля максимальной длины
        - Запрос возвращает статус 201 (Created)
        - Все переданные значения возвращаются в ответе без изменений

        Expected: Вектор должен быть успешно создан с максимальными допустимыми данными.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора с максимальными валидными значениями
        vector_data = step.data_prepare_full(data.full_max_name_vector(), data.full_max_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора
        response = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (201 Created)
        step.check_status_201(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID созданного вектора корректной длины
        step.check_response_id_len(response)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_post_response_name(response, vector_data["name"])

        # 3.4 ПРОВЕРКА: Описание вектора в ответе соответствует переданному значению
        step.check_post_response_description(response, vector_data["description"])

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_post_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: Время создания вектора соответствует текущему времени (с допустимой погрешностью)
        step.check_response_created_time(response)

        # 4. ОЧИСТКА ОКРУЖЕНИЯ: Удаление созданного вектора
        step.clean_env(self.token, response)

    @allure.title("Тест создания вектора с нормальными (типовыми) значениями полей")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(POSITIVE_TAG)
    def test_create_normal_vector(self):
        """
        POSITIVE TEST. BLOCKER severity.
        Проверяет создание вектора с нормальными (типовыми) значениями полей.

        Тест критически важен для проверки наиболее частого сценария использования.

        Что проверяет:
        - Запрос возвращает статус 201 (Created)
        - В ответе генерируется корректный ID объекта
        - Все переданные значения возвращаются в ответе без изменений

        Особенности:
        - Использует типовые значения полей (средней длины)
        - Тест самоочищается (удаляет созданный вектор после проверок)
        - Проверяет основной сценарий использования системы

        Expected: Вектор должен быть успешно создан со всеми переданными данными.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора с нормальными (типовыми) значениями
        vector_data = step.data_prepare_full(data.full_normal_name_vector(), data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора
        response = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (201 Created)
        step.check_status_201(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID созданного вектора корректной длины
        step.check_response_id_len(response)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_post_response_name(response, vector_data["name"])

        # 3.4 ПРОВЕРКА: Описание вектора в ответе соответствует переданному значению
        step.check_post_response_description(response, vector_data["description"])

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_post_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: Время создания вектора соответствует текущему времени (с допустимой погрешностью)
        step.check_response_created_time(response)

        # 4. ОЧИСТКА ОКРУЖЕНИЯ: Удаление созданного вектора
        step.clean_env(self.token, response)

    # --------------------------------------------------
    # Тесты с null-значениями
    # --------------------------------------------------

    @allure.title("Тест создания вектора с null-значением в поле name")
    @allure.severity(Severity.NORMAL)
    @allure.tag(NEGATIVE_TAG)
    def test_create_null_name_vector(self):
        """
        NEGATIVE TEST. NORMAL severity.
        Проверяет обработку системы при попытке создания вектора с null-значением в обязательном поле name.

        Что проверяет:
        - Система корректно отклоняет запрос с null-значением в обязательном поле
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке

        Особенности:
        - Проверяет валидацию обязательных полей на уровне API
        - Тест не создает данные, поэтому не требует очистки окружения

        Expected: Система должна вернуть ошибку 400 с сообщением о недопустимом null-значении.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора с null-значением в поле name
        vector_data = step.data_prepare_full(data.full_null_name_vector(), data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора
        response = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_post_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на проблему с null-значением в поле name
        step.check_post_message_name_null(response)

    @allure.title("Тест создания вектора с null-значением в поле description")
    @allure.tag(POSITIVE_TAG)
    @allure.severity(Severity.NORMAL)
    def test_create_null_description_vector(self):
        """
        POSITIVE TEST. NORMAL severity.
        Проверяет создание вектора с null-значением в необязательном поле description.

        Что проверяет:
        - Система корректно обрабатывает null-значение в необязательном поле
        - Запрос возвращает статус 201 (Created)
        - Все переданные значения возвращаются в ответе, включая null в description

        Особенности:
        - Поле description считается необязательным
        - Тест проверяет корректность обработки отсутствующих данных
        - Тест самоочищается (удаляет созданный вектор после проверок)

        Expected: Вектор должен быть успешно создан с null-значением в поле description.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора с null-значением в поле description
        vector_data = step.data_prepare_full(data.full_normal_name_vector(), data.full_null_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора
        response = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (201 Created)
        step.check_status_201(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID созданного вектора корректной длины
        step.check_response_id_len(response)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_post_response_name(response, vector_data["name"])

        # 3.4 ПРОВЕРКА: Описание вектора в ответе соответствует переданному значению
        step.check_post_response_description_null(response)

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_post_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: Время создания вектора соответствует текущему времени (с допустимой погрешностью)
        step.check_response_created_time(response)

        # 4. ОЧИСТКА ОКРУЖЕНИЯ: Удаление созданного вектора
        step.clean_env(self.token, response)
#

    @allure.title("Тест создания вектора с null-значением в поле content")
    @allure.severity(Severity.CRITICAL)
    @allure.tag(NEGATIVE_TAG)
    def test_create_null_content_vector(self):
        """
        NEGATIVE TEST. CRITICAL severity.
        Проверяет обработку системы при попытке создания вектора с null-значением в обязательном поле content.

        Что проверяет:
        - Система корректно отклоняет запрос с null-значением в обязательном поле content
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке

        Особенности:
        - Поле content является обязательным для создания вектора
        - Тест проверяет критически важную валидацию обязательных полей
        - Тест не создает данные, поэтому не требует очистки окружения

        Expected: Система должна вернуть ошибку 400 с сообщением о недопустимом null-значении в поле content.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора с null-значением в поле content
        vector_data = step.data_prepare_full(data.full_normal_name_vector(), data.full_normal_description_vector(), data.full_null_content_vector())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора
        response = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_post_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на проблему с null-значением в поле content
        step.check_post_message_content_null(response)
#
    # --------------------------------------------------
    # Тесты с недопустимыми значениями длины
    # --------------------------------------------------

    @allure.title("Тест создания вектора с недопустимой длиной имени")
    @allure.severity(Severity.NORMAL)
    @allure.tag(NEGATIVE_TAG)
    def test_create_invalid_name_vector_length(self):
        """
        NEGATIVE TEST. NORMAL severity.
        Проверяет обработку системы при попытке создания вектора с именем недопустимой длины.

        Что проверяет:
        - Система корректно отклоняет запрос с нарушением валидации длины поля name
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке валидации

        Особенности:
        - Проверяет граничные значения и валидацию длины строковых полей
        - Тест не создает данные, поэтому не требует очистки окружения
        - Ожидается четкое сообщение о нарушении ограничений длины поля

        Expected: Система должна вернуть ошибку 400 с сообщением о недопустимой длине имени.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора с именем недопустимой длины
        vector_data = step.data_prepare_full(data.full_invalid_name_vector_length(), data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора
        response = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_post_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на недопустимую длину имени
        step.check_post_message_name_invalid(response)


    #
    @allure.title("Тест создания вектора с недопустимой длиной описания")
    @allure.severity(Severity.CRITICAL)
    @allure.tag(NEGATIVE_TAG)
    def test_create_invalid_description_vector_length(self):
        """
        NEGATIVE TEST. CRITICAL severity.
        Проверяет обработку системы при попытке создания вектора с описанием недопустимой длины.

        Что проверяет:
        - Система корректно отклоняет запрос с нарушением валидации длины поля description
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке валидации

        Особенности:
        - Проверяет граничные значения и валидацию длины текстовых полей
        - Поле description может иметь критические ограничения для системы
        - Тест не создает данные, поэтому не требует очистки окружения
        - Ожидается четкое сообщение о нарушении ограничений длины поля

        Expected: Система должна вернуть ошибку 400 с сообщением о недопустимой длине описания.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора с описанием недопустимой длины
        vector_data = step.data_prepare_full(data.full_normal_name_vector(), data.full_invalid_description_vector_length(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора
        response = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_post_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на недопустимую длину описания
        step.check_post_message_description_invalid(response)

    # --------------------------------------------------
    # Тесты с недопустимыми символами
    # --------------------------------------------------

    @allure.title("Тест создания вектора с недопустимыми символами в имени")
    @allure.severity(Severity.CRITICAL)
    @allure.tag(NEGATIVE_TAG)
    def test_create_invalid_name_vector_symbols(self):
        """
        NEGATIVE TEST. CRITICAL severity.
        Проверяет обработку системы при попытке создания вектора с именем, содержащим недопустимые символы.

        Что проверяет:
        - Система корректно отклоняет запрос с нарушением валидации символов в поле name
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке валидации

        Особенности:
        - Проверяет валидацию символов и санитизацию вводимых данных
        - Защита от инъекций и некорректных данных в критически важном поле
        - Тест не создает данные, поэтому не требует очистки окружения
        - Ожидается четкое сообщение о недопустимых символах в имени

        Expected: Система должна вернуть ошибку 400 с сообщением о недопустимых символах в имени.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора с именем, содержащим недопустимые символы
        vector_data = step.data_prepare_full(data.invalid_name_symbols(), data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора
        response = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_post_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на недопустимые символы в имени
        step.check_post_message_name_invalid(response)
    # --------------------------------------------------
    # Тесты с пропущенными обязательными полями
    # --------------------------------------------------

    #
    @allure.title("Тест создания вектора без указания имени (обязательное поле)")
    @allure.severity(Severity.CRITICAL)
    @allure.tag(NEGATIVE_TAG)
    def test_create_without_name(self):
        """
        NEGATIVE TEST. CRITICAL severity.
        Проверяет обработку системы при попытке создания вектора без указания обязательного поля name.

        Что проверяет:
        - Система корректно отклоняет запрос с отсутствующим обязательным полем name
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке отсутствия обязательного поля

        Особенности:
        - Проверяет валидацию обязательных полей на уровне API
        - Тестирует обработку частично заполненных запросов
        - Тест не создает данные, поэтому не требует очистки окружения
        - Ожидается четкое сообщение об отсутствии обязательного поля name

        Expected: Система должна вернуть ошибку 400 с сообщением об отсутствии обязательного поля name.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора без указания обязательного поля name
        vector_data = step.data_prepare_without_name(data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора без поля name
        response = step.post_execute_without_name(self.token, vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_post_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на отсутствие обязательного поля name
        step.check_post_message_name_null(response)

    @allure.title("Тест создания вектора без указания описания (необязательное поле)")
    @allure.severity(Severity.NORMAL)
    @allure.tag(POSITIVE_TAG)
    def test_create_without_description(self):
        """
        POSITIVE TEST. NORMAL severity.
        Проверяет создание вектора без указания необязательного поля description.

        Что проверяет:
        - Система корректно обрабатывает запрос с отсутствующим необязательным полем description
        - Запрос возвращает статус 201 (Created)
        - Все переданные значения возвращаются в ответе, поле description может отсутствовать или быть null

        Особенности:
        - Поле description считается необязательным для создания вектора
        - Тест проверяет корректность обработки частичных данных
        - Тест самоочищается (удаляет созданный вектор после проверок)

        Expected: Вектор должен быть успешно создан без указания поля description.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора без указания необязательного поля description
        vector_data = step.data_prepare_without_description(data.full_normal_name_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора без поля description
        response = step.post_execute_without_description(self.token, vector_data["name"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (201 Created)
        step.check_status_201(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID созданного вектора корректной длины
        step.check_response_id_len(response)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_post_response_name(response, vector_data["name"])

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_post_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: В ответе нет описания
        step.check_post_response_description_null(response)

        # 3.7 ПРОВЕРКА: Время создания вектора соответствует текущему времени (с допустимой погрешностью)
        step.check_response_created_time(response)

        # 4. ОЧИСТКА ОКРУЖЕНИЯ: Удаление созданного вектора
        step.clean_env(self.token, response)

    @allure.title("Тест создания вектора без указания контента (обязательное поле)")
    @allure.severity(Severity.CRITICAL)
    @allure.tag(NEGATIVE_TAG)
    def test_create_without_content(self):
        """
        NEGATIVE TEST. CRITICAL severity.
        Проверяет обработку системы при попытке создания вектора без указания обязательного поля content.

        Что проверяет:
        - Система корректно отклоняет запрос с отсутствующим обязательным полем content
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке отсутствия обязательного поля

        Особенности:
        - Проверяет валидацию обязательных полей на уровне API
        - Поле content является критически важным для функциональности вектора
        - Тест не создает данные, поэтому не требует очистки окружения
        - Ожидается четкое сообщение об отсутствии обязательного поля content

        Expected: Система должна вернуть ошибку 400 с сообщением об отсутствии обязательного поля content.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора без указания обязательного поля content
        vector_data = step.data_prepare_without_content(data.full_normal_name_vector(), data.full_normal_description_vector())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора без поля content
        response = step.post_execute_without_content(self.token, vector_data["name"], vector_data["description"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_post_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на отсутствие обязательного поля content
        step.check_post_message_content_null(response)
    # --------------------------------------------------
    # Тесты с пробелами в полях
    # --------------------------------------------------

    @allure.title("Тест создания вектора с пробелами в имени")
    @allure.severity(Severity.NORMAL)
    @allure.tag(NEGATIVE_TAG)
    def test_create_space_name(self):
        """
        NEGATIVE TEST. NORMAL severity.
        Проверяет обработку системы при попытке создания вектора с именем, содержащим только пробелы.

        Что проверяет:
        - Система корректно отклоняет запрос с невалидным именем (только пробелы)
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке валидации имени

        Особенности:
        - Проверяет валидацию имен, состоящих только из пробельных символов
        - Тестирует обработку "пустых" значений, которые визуально не пусты
        - Тест не создает данные, поэтому не требует очистки окружения
        - Ожидается четкое сообщение о недопустимом формате имени

        Expected: Система должна вернуть ошибку 400 с сообщением о невалидном имени.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора с именем, содержащим только пробелы
        vector_data = step.data_prepare_full(data.space_name_symbols(), data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора
        response = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_post_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на невалидное имя
        step.check_post_message_name_invalid(response)

    @allure.title("Тест создания вектора с пробелами в описании")
    @allure.severity(Severity.NORMAL)
    @allure.tag(POSITIVE_TAG)
    def test_create_space_description(self):
        """
        POSITIVE TEST. NORMAL severity.
        Проверяет создание вектора без указания описания (необязательное поле).

        Что проверяет:
        - Система корректно обрабатывает запрос с отсутствующим необязательным полем description
        - Запрос возвращает статус 201 (Created)
        - Все переданные значения возвращаются в ответе, поле description отсутствует или null

        Особенности:
        - Поле description считается необязательным для создания вектора
        - Тест проверяет корректность обработки частичных данных
        - Проверяет, что поле description возвращается как null или отсутствует в ответе
        - Тест самоочищается (удаляет созданный вектор после проверок)

        Expected: Вектор должен быть успешно создан без указания поля description.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание вектора без указания необязательного поля description
        vector_data = step.data_prepare_full(data.full_normal_name_vector(), data.space_description_symbols(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка POST-запроса на создание вектора без поля description
        response = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (201 Created)
        step.check_status_201(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID созданного вектора корректной длины
        step.check_response_id_len(response)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_post_response_name(response, vector_data["name"])

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_post_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: В ответе нет описания (поле null или отсутствует)
        step.check_post_response_description_null(response)

        # 3.7 ПРОВЕРКА: Время создания вектора соответствует текущему времени (с допустимой погрешностью)
        step.check_response_created_time(response)

        # 4. ОЧИСТКА ОКРУЖЕНИЯ: Удаление созданного вектора
        step.clean_env(self.token, response)

    # --------------------------------------------------
    # Тест создания дубликата
    # --------------------------------------------------

    @allure.severity(Severity.CRITICAL)
    @allure.tag(NEGATIVE_TAG, DUPLICATE_TAG)
    @allure.title("Тест попытки создания дубликата вектора")
    @pytest.mark.usefixtures("create_vector_full")
    def test_create_dublicate(self):
        """
        NEGATIVE TEST. CRITICAL severity.
        Проверяет обработку системы при попытке создания дубликата вектора с одинаковыми данными.

        Что проверяет:
        - Система корректно отклоняет запрос на создание дубликата вектора
        - Возвращается соответствующий статус ошибки (409 Conflict)
        - Возвращается понятное сообщение об ошибке дублирования

        Особенности:
        - Использует фикстуру для предварительного создания вектора
        - Проверяет механизм защиты от дубликатов на уровне системы
        - Тест не создает новые данные, поэтому не требует дополнительной очистки
        - Ожидается четкое сообщение о конфликте дублирующихся данных

        Expected: Система должна вернуть ошибку 409 с сообщением о дубликате вектора.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ВЫПОЛНЕНИЕ ЗАПРОСА: Попытка создания дубликата вектора с теми же данными
        response = step.post_execute_full(self.token, self.vector_name, self.vector_description, self.vector_content)

        # 2.1 ПРОВЕРКА: Запрос отклонен с ошибкой 409 (Conflict)
        step.check_post_status_409(response)

        # 2.2 ПРОВЕРКА: Сообщение об ошибке указывает на дубликат вектора
        step.check_post_message_dublicate(response)

#
#
# # Сделать тесты для content
#
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("PATCH VECTOR")
@allure.parent_suite(PARENT_SUITE)
@allure.suite(SUITE)
@allure.tag("api", "rest", "vector", "update")
@allure.label(LabelType.LANGUAGE, "python")
@allure.label(LabelType.FRAMEWORK, "pytest")
@allure.link(
   TEST_REPO,
    name="Ссылка на репозиторий с тестами",
)
@allure.link(
   SWAGGER, name="Ссылка на swagger с методами для Vector"
)
@pytest.mark.usefixtures("get_token", "create_vector_full")

class TestPatchVector:
    """
    Класс тестов для проверки обновления векторов через PATCH-запросы

    Использует фикстуры:
    - get_token: для получения JWT токена авторизации
    - create_vector_full: для создания тестового вектора перед каждым тестом

    Содержит тесты:
    - С валидными данными (минимальные, максимальные, нормальные значения)
    - С некорректными данными (null, недопустимая длина, спецсимволы)
    - Граничные случаи (пропуск обязательных полей, пробелы, дубликаты)
    - Проверки временной метки обновления
    """

    # --------------------------------------------------
    # Тесты с валидными данными
    # --------------------------------------------------

    @allure.title("Тест обновления вектора с минимально допустимыми значениями полей")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(POSITIVE_TAG)
    @pytest.mark.flaky(reruns=10, reruns_delay=1)
    def test_patch_min_vector(self):
        """
        POSITIVE TEST. BLOCKER severity.
        Проверяет обновление вектора с минимально допустимыми значениями полей.

        Что проверяет:
        - Запрос на обновление возвращает статус 200 (OK)
        - ID вектора в ответе соответствует обновляемому объекту
        - Все обновленные значения возвращаются в ответе без изменений
        - Время обновления корректно устанавливается

        Особенности:
        - Использует минимальные валидные значения для всех полей
        - Настроены повторные запуски при падении (10 попыток с задержкой 1 сек)
        - Проверяет корректность работы механизма обновления

        Expected: Вектор должен быть успешно обновлен со всеми переданными данными.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных с минимальными валидными значениями
        vector_data = step.data_prepare_full(data.full_min_name_vector(), data.full_min_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (200 OK)
        step.check_status_200(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID обновленного вектора
        step.check_patch_response_id(response, self.vector_id)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_patch_response_name(response, vector_data["name"])

        # 3.4 ПРОВЕРКА: Описание вектора в ответе соответствует переданному значению
        step.check_patch_response_description(response, vector_data["description"])

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_patch_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: Время обновления вектора соответствует текущему времени
        step.check_response_updated_time(response)

    @allure.title("Тест обновления вектора с максимально допустимыми значениями полей")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(POSITIVE_TAG)
    def test_patch_max_vector(self):
        """
        POSITIVE TEST. BLOCKER severity.
        Проверяет обновление вектора с максимально допустимыми значениями полей.

        Что проверяет:
        - Запрос на обновление возвращает статус 200 (OK)
        - ID вектора в ответе соответствует обновляемому объекту
        - Все обновленные значения возвращаются в ответе без изменений
        - Время обновления корректно устанавливается

        Особенности:
        - Использует максимальные валидные значения для всех полей
        - Проверяет верхние границы допустимых значений при обновлении
        - Тестирует обработку длинных данных в системе

        Expected: Вектор должен быть успешно обновлен с максимальными допустимыми данными.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных с максимальными валидными значениями
        vector_data = step.data_prepare_full(data.full_max_name_vector(), data.full_max_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (200 OK)
        step.check_status_200(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID обновленного вектора
        step.check_patch_response_id(response, self.vector_id)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_patch_response_name(response, vector_data["name"])

        # 3.4 ПРОВЕРКА: Описание вектора в ответе соответствует переданному значению
        step.check_patch_response_description(response, vector_data["description"])

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_patch_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: Время обновления вектора соответствует текущему времени
        step.check_response_updated_time(response)

    @allure.title("Тест обновления вектора с нормальными (типовыми) значениями полей")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(POSITIVE_TAG)
    def test_patch_normal_vector(self):
        """
        POSITIVE TEST. BLOCKER severity.
        Проверяет обновление вектора с нормальными (типовыми) значениями полей.

        Что проверяет:
        - Запрос на обновление возвращает статус 200 (OK)
        - ID вектора в ответе соответствует обновляемому объекту
        - Все обновленные значения возвращаются в ответе без изменений
        - Время обновления корректно устанавливается

        Особенности:
        - Использует типовые значения полей (средней длины)
        - Проверяет основной сценарий использования системы
        - Тестирует наиболее частый случай обновления данных

        Expected: Вектор должен быть успешно обновлен с типовыми данными.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных с нормальными значениями
        vector_data = step.data_prepare_full(data.full_normal_name_vector(), data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (200 OK)
        step.check_status_200(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID обновленного вектора
        step.check_patch_response_id(response, self.vector_id)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_patch_response_name(response, vector_data["name"])

        # 3.4 ПРОВЕРКА: Описание вектора в ответе соответствует переданному значению
        step.check_patch_response_description(response, vector_data["description"])

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_patch_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: Время обновления вектора соответствует текущему времени
        step.check_response_updated_time(response)



    # --------------------------------------------------
    # Тесты с null-значениями
    # --------------------------------------------------

    @allure.title("Тест обновления вектора с null-значением в поле name")
    @allure.severity(Severity.NORMAL)
    @allure.tag(NEGATIVE_TAG)
    def test_patch_null_name_vector(self):
        """
        NEGATIVE TEST. NORMAL severity.
        Проверяет обработку системы при попытке обновления вектора с null-значением в обязательном поле name.

        Что проверяет:
        - Система корректно отклоняет запрос с null-значением в обязательном поле
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке

        Особенности:
        - Проверяет валидацию обязательных полей при обновлении
        - Тест не изменяет данные, поэтому не требует отката изменений
        - Ожидается четкое сообщение о недопустимом null-значении

        Expected: Система должна вернуть ошибку 400 с сообщением о недопустимом null-значении в поле name.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных с null-значением в поле name
        vector_data = step.data_prepare_full(data.full_null_name_vector(), data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_patch_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на проблему с null-значением в поле name
        step.check_patch_message_name_null(response)

    @allure.title("Тест обновления вектора с null-значением в поле description")
    @allure.severity(Severity.NORMAL)
    @allure.tag(POSITIVE_TAG)
    def test_patch_null_description_vector(self):
        """
        POSITIVE TEST. NORMAL severity.
        Проверяет обновление вектора с null-значением в необязательном поле description.

        Что проверяет:
        - Запрос на обновление возвращает статус 200 (OK)
        - ID вектора в ответе соответствует обновляемому объекту
        - Поле description корректно обновляется на null-значение
        - Время обновления корректно устанавливается

        Особенности:
        - Поле description считается необязательным при обновлении
        - Проверяет корректность обработки null-значений в необязательных полях
        - Тестирует сценарий очистки поля description

        Expected: Вектор должен быть успешно обновлен с null-значением в поле description.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных с null-значением в поле description
        vector_data = step.data_prepare_full(data.full_normal_name_vector(), data.full_null_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (200 OK)
        step.check_status_200(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID обновленного вектора
        step.check_patch_response_id(response, self.vector_id)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_patch_response_name(response, vector_data["name"])

        # 3.4 ПРОВЕРКА: Описание вектора в ответе соответствует null-значению
        step.check_patch_response_description_null(response)

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_patch_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: Время обновления вектора соответствует текущему времени
        step.check_response_updated_time(response)

    @allure.title("Тест обновления вектора с null-значением в поле content")
    @allure.severity(Severity.CRITICAL)
    @allure.tag(NEGATIVE_TAG)
    def test_patch_null_content_vector(self):
        """
        NEGATIVE TEST. CRITICAL severity.
        Проверяет обработку системы при попытке обновления вектора с null-значением в обязательном поле content.

        Что проверяет:
        - Система корректно отклоняет запрос с null-значением в обязательном поле
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке

        Особенности:
        - Поле content является обязательным при обновлении
        - Проверяет критически важную валидацию обязательных полей
        - Тест не изменяет данные, поэтому не требует отката изменений

        Expected: Система должна вернуть ошибку 400 с сообщением о недопустимом null-значении в поле content.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных с null-значением в поле content
        vector_data = step.data_prepare_full(data.full_normal_name_vector(), data.full_normal_description_vector(), data.full_null_content_vector())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_patch_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на проблему с null-значением в поле content
        step.check_patch_message_content_null(response)




    # --------------------------------------------------
    # Тесты с недопустимыми значениями длины
    # --------------------------------------------------

    @allure.title("Тест обновления вектора с недопустимой длиной имени")
    @allure.severity(Severity.NORMAL)
    @allure.tag(NEGATIVE_TAG)
    def test_patch_invalid_name_vector_length(self):
        """
        NEGATIVE TEST. NORMAL severity.
        Проверяет обработку системы при попытке обновления вектора с именем недопустимой длины.

        Что проверяет:
        - Система корректно отклоняет запрос с нарушением валидации длины поля name
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке валидации

        Особенности:
        - Проверяет граничные значения и валидацию длины при обновлении
        - Тест не изменяет данные, поэтому не требует отката изменений
        - Ожидается четкое сообщение о нарушении ограничений длины поля name

        Expected: Система должна вернуть ошибку 400 с сообщением о недопустимой длине имени.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных с именем недопустимой длины
        vector_data = step.data_prepare_full(data.full_invalid_name_vector_length(), data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_patch_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на недопустимую длину имени
        step.check_patch_message_name_invalid(response)

    @allure.title("Тест обновления вектора с недопустимой длиной описания")
    @allure.severity(Severity.NORMAL)
    @allure.tag(NEGATIVE_TAG)
    def test_patch_invalid_description_vector_length(self):
        """
        NEGATIVE TEST. NORMAL severity.
        Проверяет обработку системы при попытке обновления вектора с описанием недопустимой длины.

        Что проверяет:
        - Система корректно отклоняет запрос с нарушением валидации длины поля description
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке валидации

        Особенности:
        - Проверяет граничные значения и валидацию длины при обновлении
        - Тест не изменяет данные, поэтому не требует отката изменений
        - Ожидается четкое сообщение о нарушении ограничений длины поля description

        Expected: Система должна вернуть ошибку 400 с сообщением о недопустимой длине описания.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных с описанием недопустимой длины
        vector_data = step.data_prepare_full(data.full_normal_name_vector(), data.full_invalid_description_vector_length(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_patch_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на недопустимую длину описания
        step.check_patch_message_description_invalid(response)




    # --------------------------------------------------
    # Тесты с недопустимыми символами
    # --------------------------------------------------
    @allure.title("Тест обновления вектора с недопустимыми символами в имени")
    @allure.severity(Severity.CRITICAL)
    @allure.tag(NEGATIVE_TAG)
    def test_patch_invalid_name_vector_symbols(self):
        """
        NEGATIVE TEST. CRITICAL severity.
        Проверяет обработку системы при попытке обновления вектора с именем, содержащим недопустимые символы.

        Что проверяет:
        - Система корректно отклоняет запрос с нарушением валидации символов в поле name
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке валидации

        Особенности:
        - Проверяет валидацию символов и санитизацию при обновлении данных
        - Защита от инъекций и некорректных данных в критически важном поле
        - Тест не изменяет данные, поэтому не требует отката изменений
        - Ожидается четкое сообщение о недопустимых символах в имени

        Expected: Система должна вернуть ошибку 400 с сообщением о недопустимых символах в имени.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных с именем, содержащим недопустимые символы
        vector_data = step.data_prepare_full(data.invalid_name_symbols(), data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_patch_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на недопустимые символы в имени
        step.check_patch_message_name_invalid(response)

    # --------------------------------------------------
    # Тесты с пропущенными полями
    # --------------------------------------------------

    @allure.title("Тест обновления вектора без указания имени")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(NEGATIVE_TAG)
    def test_patch_without_name(self):
        """
        NEGATIVE TEST. BLOCKER severity.
        Проверяет обработку системы при попытке обновления вектора без указания обязательного поля name.

        Что проверяет:
        - Система корректно отклоняет запрос с отсутствующим обязательным полем name
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке отсутствия обязательного поля

        Особенности:
        - Проверяет валидацию обязательных полей при обновлении на уровне API
        - Тестирует обработку частично заполненных запросов на обновление
        - Тест не изменяет данные, поэтому не требует отката изменений

        Expected: Система должна вернуть ошибку 400 с сообщением об отсутствии обязательного поля name.
        """

        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных без указания обязательного поля name
        vector_data = step.data_prepare_without_name(data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора без поля name
        response = step.patch_execute_without_name(self.token, self.vector_id, vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_patch_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на отсутствие обязательного поля name
        step.check_patch_message_name_null(response)

    @allure.title("Тест обновления вектора без указания описания")
    @allure.severity(Severity.NORMAL)
    @allure.tag(POSITIVE_TAG)
    def test_patch_without_description(self):
        """
        POSITIVE TEST. NORMAL severity.
        Проверяет обновление вектора без указания необязательного поля description.

        Что проверяет:
        - Запрос на обновление возвращает статус 200 (OK)
        - ID вектора в ответе соответствует обновляемому объекту
        - Поле description корректно обрабатывается как отсутствующее
        - Время обновления корректно устанавливается

        Особенности:
        - Поле description считается необязательным при обновлении
        - Проверяет корректность обработки частичных данных при обновлении
        - Тестирует сценарий, когда поле description не передается

        Expected: Вектор должен быть успешно обновлен без указания поля description.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных без указания необязательного поля description
        vector_data = step.data_prepare_without_description(data.full_normal_name_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора без поля description
        response = step.patch_execute_without_description(self.token, self.vector_id, vector_data["name"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (200 OK)
        step.check_status_200(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID обновленного вектора
        step.check_patch_response_id(response, self.vector_id)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_patch_response_name(response, vector_data["name"])

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_patch_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: В ответе нет описания (поле null или отсутствует)
        step.check_patch_response_description_null(response)

        # 3.7 ПРОВЕРКА: Время обновления вектора соответствует текущему времени
        step.check_response_updated_time(response)

    @allure.title("Тест обновления вектора без указания контента")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(NEGATIVE_TAG)
    def test_patch_without_content(self):
        """
        NEGATIVE TEST. BLOCKER severity.
        Проверяет обработку системы при попытке обновления вектора без указания обязательного поля content.

        Что проверяет:
        - Система корректно отклоняет запрос с отсутствующим обязательным полем content
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке отсутствия обязательного поля

        Особенности:
        - Поле content является обязательным при обновлении
        - Проверяет критически важную валидацию обязательных полей
        - Тест не изменяет данные, поэтому не требует отката изменений

        Expected: Система должна вернуть ошибку 400 с сообщением об отсутствии обязательного поля content.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных без указания обязательного поля content
        vector_data = step.data_prepare_without_content(data.full_normal_name_vector(), data.full_normal_description_vector())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора без поля content
        response = step.patch_execute_without_content(self.token, self.vector_id, vector_data["name"], vector_data["description"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_patch_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на отсутствие обязательного поля content
        step.check_patch_message_content_null(response)
    # --------------------------------------------------
    # Тесты с пробелами в полях
    # --------------------------------------------------

    @allure.title("Тест обновления вектора с пробелами в имени")
    @allure.severity(Severity.NORMAL)
    @allure.tag(NEGATIVE_TAG)
    def test_patch_space_name(self):
        """
        NEGATIVE TEST. NORMAL severity.
        Проверяет обработку системы при попытке обновления вектора с именем, содержащим только пробелы.

        Что проверяет:
        - Система корректно отклоняет запрос с невалидным именем (только пробелы)
        - Возвращается соответствующий статус ошибки (400 Bad Request)
        - Возвращается понятное сообщение об ошибке валидации имени

        Особенности:
        - Проверяет валидацию имен, состоящих только из пробельных символов при обновлении
        - Тестирует обработку "пустых" значений, которые визуально не пусты
        - Тест не изменяет данные, поэтому не требует отката изменений

        Expected: Система должна вернуть ошибку 400 с сообщением о невалидном имени.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных с именем, содержащим только пробелы
        vector_data = step.data_prepare_full(data.space_name_symbols(), data.full_normal_description_vector(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_patch_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на невалидное имя
        step.check_patch_message_name_invalid(response)

    @allure.title("Тест обновления вектора с пробелами в описании")
    @allure.severity(Severity.NORMAL)
    @allure.tag(POSITIVE_TAG)
    def test_patch_space_description(self):
        """
        POSITIVE TEST. NORMAL severity.
        Проверяет обновление вектора с описанием, содержащим только пробелы.

        Что проверяет:
        - Запрос на обновление возвращает статус 200 (OK)
        - ID вектора в ответе соответствует обновляемому объекту
        - Поле description корректно обрабатывается при пробельных значениях
        - Время обновления корректно устанавливается

        Особенности:
        - Поле description может содержать пробельные символы
        - Проверяет корректность обработки пробелов в необязательных полях
        - Тестирует сценарий, когда поле description состоит только из пробелов

        Expected: Вектор должен быть успешно обновлен с пробелами в поле description.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка данных с описанием, содержащим пробелы
        vector_data = step.data_prepare_full(data.full_normal_name_vector(), data.space_description_symbols(), data.full_vector_content())

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка PATCH-запроса на обновление вектора
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (200 OK)
        step.check_status_200(response)

        # 3.2 ПРОВЕРКА: В ответе присутствует ID обновленного вектора
        step.check_patch_response_id(response, self.vector_id)

        # 3.3 ПРОВЕРКА: Имя вектора в ответе соответствует переданному значению
        step.check_patch_response_name(response, vector_data["name"])

        # 3.5 ПРОВЕРКА: Контент вектора в ответе соответствует переданному значению
        step.check_patch_response_content(response, vector_data["content"])

        # 3.6 ПРОВЕРКА: Описание в ответе обработано корректно (null или пробелы)
        step.check_patch_response_description_null(response)

        # 3.7 ПРОВЕРКА: Время обновления вектора соответствует текущему времени
        step.check_response_updated_time(response)


    # --------------------------------------------------
    # Тест создания дубликата
    # --------------------------------------------------

    @allure.title("Тест попытки обновления вектора с созданием дубликата")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(NEGATIVE_TAG)
    def test_patch_dublicate(self):
        """
        NEGATIVE TEST. BLOCKER severity.
        Проверяет обработку системы при попытке обновления вектора с данными, которые создадут дубликат существующего вектора.

        Что проверяет:
        - Система корректно отклоняет запрос на обновление, который приведет к созданию дубликата
        - Возвращается соответствующий статус ошибки (409 Conflict)
        - Возвращается понятное сообщение об ошибке дублирования

        Особенности:
        - Сначала создается отдельный вектор-дубликат для проверки конфликта
        - Проверяет механизм защиты от дубликатов при обновлении данных
        - Тест не изменяет исходные данные, поэтому не требует отката изменений

        Expected: Система должна вернуть ошибку 409 с сообщением о дубликате вектора.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Создание отдельного вектора-дубликата для проверки конфликта
        vector_data = step.data_prepare_full(data.full_normal_name_vector(), data.full_normal_description_vector(), data.full_vector_content())
        vector = step.post_execute_full(self.token, vector_data["name"], vector_data["description"], vector_data["content"])

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Попытка обновления текущего вектора данными, которые создадут дубликат
        response = step.patch_execute_full(self.token, self.vector_id, vector_data["name"], vector_data["description"], vector_data["content"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 409 (Conflict)
        step.check_patch_status_409(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на дубликат вектора
        step.check_patch_message_dublicate(response)

        # 4. ОЧИСТКА ОКРУЖЕНИЯ: Удаление созданного вектора
        step.clean_env(self.token, vector)


#
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("GET VECTOR")
@allure.parent_suite(PARENT_SUITE)
@allure.suite(SUITE)
@allure.tag("api", "rest", "vector", "read")
@allure.label(LabelType.LANGUAGE, "python")
@allure.label(LabelType.FRAMEWORK, "pytest")
@allure.link(
   TEST_REPO,
    name="Ссылка на репозиторий с тестами",
)
@allure.link(
   SWAGGER, name="Ссылка на swagger с методами для Vector"
)
@pytest.mark.usefixtures("get_token", "create_vector_full")
class TestGetVector:
    """
    Test Suite: Тесты получения векторов (GET-запросы)

    Фикстуры:
    - get_token: получение токена аутентификации
    - create_vector_full: создание тестового вектора перед каждым тестом

    Область покрытия:
    - Получение списка всех векторов
    - Получение конкретного вектора по ID
    - Работа с параметрами пагинации (page, limit)
    - Поиск векторов через параметр q (по имени и описанию)
    - Обработка ошибок при невалидных параметрах
    """

    @allure.title("Тест получения списка векторов")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(POSITIVE_TAG)
    def test_get_vector(self):
        """
        POSITIVE TEST. BLOCKER severity.
        Проверяет корректное получение списка всех векторов из системы.

        Что проверяет:
        - Запрос на получение списка возвращает статус 200 (OK)
        - Ответ содержит валидную структуру данных со списком векторов

        Особенности:
        - Проверяет работу основного read-метода API
        - Критически важен для обеспечения доступа к данным

        Expected: Система должна вернуть корректный список векторов со статусом 200.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка GET-запроса на получение списка векторов
        response = step.get_execute(self.token)

        # 2.1 ПРОВЕРКА: Запрос на получение списка успешно обработан (200 OK)
        step.check_get_status_200(response)

    @allure.title("Тест получения конкретного вектора по ID")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(POSITIVE_TAG)
    def test_get_vector_id(self):
        """
        POSITIVE TEST. BLOCKER severity.
        Проверяет корректное получение конкретного вектора по его идентификатору.

        Что проверяет:
        - Запрос на получение вектора по ID возвращает статус 200 (OK)
        - Все поля вектора в ответе соответствуют ожидаемым значениям
        - Время создания корректно отображается

        Особенности:
        - Проверяет точность данных при получении по ID
        - Валидирует все основные поля вектора

        Expected: Система должна вернуть корректные данные вектора со статусом 200.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка GET-запроса на получение вектора по ID
        response = step.get_id_execute(self.token, self.vector_id)

        # 2.1 ПРОВЕРКА: Запрос успешно обработан (200 OK)
        step.check_get_status_200(response)

        # 2.2 ПРОВЕРКА: ID вектора в ответе соответствует запрошенному
        step.check_get_response_id(response, self.vector_id)

        # 2.3 ПРОВЕРКА: Имя вектора в ответе соответствует ожидаемому
        step.check_get_response_name(response, self.vector_name)

        # 2.4 ПРОВЕРКА: Описание вектора в ответе соответствует ожидаемому
        step.check_get_response_description(response, self.vector_description)

        # 2.5 ПРОВЕРКА: Контент вектора в ответе соответствует ожидаемому
        step.check_get_response_content(response, self.vector_content)

        # 2.6 ПРОВЕРКА: Время создания вектора корректно отображается
        step.check_response_created_time(response)

    @allure.title("Тест работы параметров page и limit с валидными значениями")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(POSITIVE_TAG)
    def test_get_vector_normal_page_limit(self):
        """
        POSITIVE TEST. BLOCKER severity.
        Проверяет корректную работу пагинации с валидными значениями page и limit.

        Что проверяет:
        - Запрос с параметрами пагинации возвращает статус 200 (OK)
        - Система корректно обрабатывает валидные значения page и limit

        Особенности:
        - Тестирует механизм разбиения данных на страницы
        - Проверяет ограничение количества элементов на странице

        Expected: Система должна вернуть данные с корректной пагинацией.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка параметров пагинации
        gp = step.get_parameters_prepare(data_len.normal_page_vector_length(), data_len.normal_limit_vector_length(), "")

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка GET-запроса с параметрами page и limit
        response = step.get_execute_page_limit_q(self.token, gp["page"], gp["limit"], gp["q"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (200 OK)
        step.check_get_status_200(response)

    @allure.title("Тест отправки невалидного значения 0 в параметр page")
    @allure.severity(Severity.NORMAL)
    @allure.tag(NEGATIVE_TAG)
    def test_get_vector_zero_page(self):
        """
        NEGATIVE TEST. NORMAL severity.
        Проверяет обработку невалидного значения 0 в параметре page.

        Что проверяет:
        - Запрос с page=0 возвращает статус 400 (Bad Request)
        - Возвращается понятное сообщение об ошибке

        Особенности:
        - Проверяет валидацию входных параметров пагинации
        - Тестирует обработку граничных значений

        Expected: Система должна вернуть ошибку 400 с сообщением о невалидном page.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка параметров с невалидным page=0
        gp = step.get_parameters_prepare(data_len.invalid_page_vector_length(), data_len.normal_limit_vector_length(), "")

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка GET-запроса с невалидным page
        response = step.get_execute_page_limit_q(self.token, gp["page"], gp["limit"], gp["q"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_get_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на проблему с page или limit
        step.check_message_null_page_or_limit(response)

    @allure.title("Тест отправки невалидного значения 0 в параметр limit")
    @allure.severity(Severity.NORMAL)
    @allure.tag(NEGATIVE_TAG)
    def test_get_vector_zero_limit(self):
        """
        NEGATIVE TEST. NORMAL severity.
        Проверяет обработку невалидного значения 0 в параметре limit.

        Что проверяет:
        - Запрос с limit=0 возвращает статус 400 (Bad Request)
        - Возвращается понятное сообщение об ошибке

        Особенности:
        - Проверяет валидацию входных параметров пагинации
        - Тестирует обработку граничных значений

        Expected: Система должна вернуть ошибку 400 с сообщением о невалидном limit.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка параметров с невалидным limit=0
        gp = step.get_parameters_prepare(data_len.normal_page_vector_length(), data_len.invalid_limit_vector_length(), "")

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка GET-запроса с невалидным limit
        response = step.get_execute_page_limit_q(self.token, gp["page"], gp["limit"], gp["q"])

        # 3.1 ПРОВЕРКА: Запрос отклонен с ошибкой 400 (Bad Request)
        step.check_get_status_400(response)

        # 3.2 ПРОВЕРКА: Сообщение об ошибке указывает на проблему с page или limit
        step.check_message_null_page_or_limit(response)

    @allure.title("Тест поиска векторов по названию через параметр q")
    @allure.severity(Severity.CRITICAL)
    @allure.tag(POSITIVE_TAG)
    def test_get_vector_q_name(self):
        """
        POSITIVE TEST. CRITICAL severity.
        Проверяет поиск векторов по полному совпадению названия.

        Что проверяет:
        - Запрос с параметром q возвращает статус 200 (OK)
        - Найденные векторы соответствуют поисковому запросу
        - Поиск работает корректно по полю name

        Особенности:
        - Тестирует функционал поиска по имени
        - Критически важен для пользовательского поиска

        Expected: Система должна вернуть векторы, соответствующие поисковому запросу.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка параметров запроса с поиском по имени
        gp = step.get_parameters_prepare(data_len.min_page_vector_length(), data_len.normal_limit_vector_length(), self.vector_name)

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка GET-запроса с параметром поиска q
        response = step.get_execute_page_limit_q(self.token, gp["page"], gp["limit"], gp["q"])

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (200 OK)
        step.check_get_status_200(response)

        # 3.2 ПРОВЕРКА: Найденные векторы соответствуют поисковому запросу по имени
        step.check_response_q_name(response, gp["q"])

    @allure.title("Тест поиска векторов по описанию через параметр q")
    @allure.severity(Severity.CRITICAL)
    @allure.tag(POSITIVE_TAG)
    @pytest.mark.skip  # скипать до устранения бага https://jira.astralinux.ru/browse/MON-2459
    @allure.link("https://jira.astralinux.ru/browse/MON-2459", name="Тест пропускается из-за бага mon-2459")
    # @pytest.mark.flaky(reruns=3, reruns_delay=2,
    #                    rerun_exceptions=(IndexError, AssertionError))
    def test_get_vector_q_description(self):
        """
        POSITIVE TEST. CRITICAL severity.
        Проверяет поиск векторов по описанию через параметр q.

        Что проверяет:
        - Запрос с параметром q возвращает статус 200 (OK)
        - Найденные векторы соответствуют поисковому запросу в описании
        - Поиск работает корректно по полю description

        Особенности:
        - Временно отключен из-за бага MON-2459
        - Настроены повторные запуски для обработки нестабильности
        - Тестирует поиск по текстовому полю description

        Expected: Система должна вернуть векторы, соответствующие поисковому запросу в описании.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ПОДГОТОВКА ДАННЫХ: Подготовка параметров запроса с поиском по описанию
        gp = step.get_parameters_prepare(data_len.min_page_vector_length(), data_len.max_limit_vector_length(), self.vector_description)

        # 2. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка GET-запроса с параметром поиска q
        response = step.get_execute_page_limit_q(self.token, gp["page"], gp["limit"], self.vector_description)

        # 3.1 ПРОВЕРКА: Запрос успешно обработан (200 OK)
        step.check_get_status_200(response)

        # 3.2 ПРОВЕРКА: Найденные векторы соответствуют поисковому запросу по описанию
        step.check_response_q_description(response, gp["q"])
#
@allure.epic(EPIC)
@allure.feature(FEATURE)
@allure.story("DELETE VECTOR")
@allure.parent_suite(PARENT_SUITE)
@allure.suite(SUITE)
@allure.tag("api", "rest", "vector", "delete")
@allure.label(LabelType.LANGUAGE, "python")
@allure.label(LabelType.FRAMEWORK, "pytest")
@allure.link(
   TEST_REPO,
    name="Ссылка на репозиторий с тестами",
)
@allure.link(
   SWAGGER, name="Ссылка на swagger с методами для Vector"
)
@pytest.mark.usefixtures("get_token", "create_vector_full", "create_release_vector")
class TestDeleteVector:
    """
    Класс тестов для проверки удаления векторов через DELETE-запросы

    Использует фикстуры:
    - get_token: для получения JWT токена авторизации
    - create_vector_full: создает тестовый вектор перед выполнением тестов

    Содержит тесты:
    - Удаления вектора по ID
    - Проверки факта удаления
    """

    @allure.title("Тест удаления вектора")
    @allure.severity(Severity.BLOCKER)
    @allure.tag(POSITIVE_TAG)
    def test_delete_vector(self):
        """
        POSITIVE TEST. BLOCKER severity.
        Проверяет корректное удаление вектора из системы.

        Что проверяет:
        - Запрос на удаление возвращает статус 204 (No Content)
        - Вектор действительно удаляется из системы
        - Последующие попытки доступа к удаленному вектору возвращают ошибку 404

        Особенности:
        - Проверяет полноту удаления данных
        - Тестирует механизм очистки ресурсов
        - Критически важен для обеспечения целостности данных

        Expected: Вектор должен быть полностью удален из системы.
        """
        # ШАГИ ВЫПОЛНЕНИЯ:
        # 1. ВЫПОЛНЕНИЕ ЗАПРОСА: Отправка DELETE-запроса на удаление вектора
        response = step.delete_execute(self.token, self.vector_id)

        # 2.1 ПРОВЕРКА: Запрос на удаление успешно обработан (204 No Content)
        step.check_status_204(response)

        # 2.2 ПРОВЕРКА: Вектор действительно удален - запрос к нему возвращает 404
        response = step.get_id_execute(self.token, self.vector_id)
        step.check_message_not_found(response)


