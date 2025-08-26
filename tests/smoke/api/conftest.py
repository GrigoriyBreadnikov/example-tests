import httpx
import pytest
import time
from typing import Any, Dict, Optional
from smoke.api.config import env
transport = httpx.HTTPTransport(retries=3)
client = httpx.Client(transport=transport)
@pytest.fixture(scope="class")
def get_token(request: pytest.FixtureRequest) -> str:
    """
    Фикстура для получения OAuth токена доступа.

    Выполняет POST-запрос к эндпоинту авторизации с учетными данными из конфигурации.
    Сохраняет полученный токен в атрибуте request.cls.token для использования в тестах.

    Args:
        request: Объект pytest FixtureRequest для доступа к контексту теста

    Returns:
        Строка с access token

    Raises:
        httpx.HTTPError: При ошибках HTTP запроса
        KeyError: Если в ответе отсутствует access_token
        Exception: При других непредвиденных ошибках

    Note:
        Отключает верификацию SSL (verify=False) - не используйте в production!

    Configuration Requirements:
        В модуле V должны быть определены:
        - TOKEN_URL: URL эндпоинта авторизации
        - GRANT_TYPE: Тип OAuth гранта (например "password")
        - USERNAME: Имя пользователя
        - PASSWORD: Пароль
        - SCOPE: Области доступа
        - CLIENT_ID: Идентификатор клиента
        - SECRET: Секрет клиента
    """
    headers: Dict[str, str] = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload: Dict[str, str] = {
        "grant_type": env.GRANT_TYPE,
        "username": env.USERNAME,
        "password": env.PASSWORD,
        "scope": env.SCOPE,
        "client_id": env.CLIENT_ID,
        "client_secret": env.SECRET
    }

    try:
        response = httpx.post(
            url=env.TOKEN_URL,
            headers=headers,
            data=payload,
            verify=False
        )
        response.raise_for_status()
        response_json: Dict[str, Any] = response.json()
        token: str = response_json['access_token']
        request.cls.token = token

        print("URL запроса:", env.TOKEN_URL)
        print(f"Получен токен: {token[:10]}...")
        return token
    except httpx.HTTPError as e:
        print(f"Ошибка HTTP при получении токена: {e}")
        raise
    except KeyError:
        print("Ошибка: отсутствует access_token в ответе")
        raise
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        raise



@pytest.fixture(scope="session")
def cache(pytestconfig: pytest.Config) -> Optional[pytest.Cache]:
    """
    Фикстура для доступа к кешу pytest в рамках сессии.

    Args:
        pytestconfig: Конфигурация pytest

    Returns:
        Объект pytest.Cache или None, если кеш недоступен

    Note:
        Автоматически используется во всех тестах (autouse=True)
        Сохраняет данные между запусками тестов
    """
    return pytestconfig.cache

# @pytest.fixture(scope="function", autouse=True)
# def delay_between_tests():
#     yield
#     time.sleep(5)