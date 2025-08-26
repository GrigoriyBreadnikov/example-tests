import pytest
from typing import Any, Dict
from smoke.api.main import GeneralFunctions
from smoke.api.vector.rest import VectorRequestBody, VectorPost, VectorResponse, VectorDelete
from smoke.api.vector.tests.faker import VectorFullData

# Инициализация вспомогательных классов
GF: GeneralFunctions = GeneralFunctions()
VP: VectorPost = VectorPost()
VB: VectorRequestBody = VectorRequestBody()
Res: VectorResponse = VectorResponse()
VFD: VectorFullData = VectorFullData()
VD: VectorDelete = VectorDelete()


@pytest.fixture(scope="function")
def create_vector_full(request: pytest.FixtureRequest, get_token: str) -> Dict[str, Any]:
    """
    Фикстура для создания тестового вектора с полным набором данных.

    Создает вектор с валидными данными:
    - name: сгенерированное нормальное имя вектора
    - description: сгенерированное нормальное описание
    - content: сгенерированное содержимое вектора

    Сохраняет данные созданного вектора в атрибутах тестового класса:
    - vector_id: ID созданного вектора
    - vector_name: имя вектора
    - vector_description: описание вектора
    - vector_content: содержимое вектора

    Args:
        request: Объект pytest FixtureRequest для доступа к контексту теста
        get_token: Фикстура, возвращающая валидный токен авторизации (str)

    Returns:
        Dict[str, Any]: Полный ответ API после создания вектора в формате словаря

    Example:
        class TestVector:
            def test_vector_operations(self, create_vector_full):
                print(f"Testing vector with ID: {self.vector_id}")
                assert self.vector_name is not None
    """
    # Генерация тестовых данных
    name: str = VFD.full_normal_name_vector()
    description: str = VFD.full_normal_description_vector()
    content: str = VFD.full_vector_content()

    # Создание вектора через API и получение ответа
    response: Dict[str, Any] = Res.get_response_vector(
        VP.post_vector(get_token, name, description, content)
    )

    # Извлечение данных из ответа
    id: str = response["response"]["id"]
    name = response["response"]["name"]
    description = response["response"]["description"]
    content = response["response"]["content"]

    # Сохранение данных в атрибутах тестового класса
    request.cls.vector_id = id
    request.cls.vector_name = name
    request.cls.vector_description = description
    request.cls.vector_content = content

    # return response
    yield response
    # Очистка ресурса после завершения теста
    VD.delete_vector(get_token, id)

@pytest.fixture(scope="function")
def create_release_vector(get_token: str) :
    """
    Фикстура для создания вектора для тестирования в релизной версии с полным набором данных.

    Создает вектор с валидными данными:
    - name: указано фиксированное имя вектора
    - description: указано фиксированное описание
    - content: указано фиксированное содержимое вектора

    """
    # Тестовых данные
    name: str = "test_release.yaml"
    description: str = "Файл вектор для тестирования логов в релизе"
    content: str = VFD.full_vector_content()

    # Создание вектора через API и получение ответа
    VP.post_vector(get_token, name, description, content)

