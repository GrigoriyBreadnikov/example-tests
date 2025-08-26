import httpx
from typing import Any, Dict
import logging


class RequestModel:
    """
    Класс для выполнения HTTP-запросов с базовой конфигурацией.
    Предоставляет статические методы для POST, PATCH, GET, DELETE запросов.
    """

    @staticmethod
    def post(url: str, token: str, body_post: Dict[str, Any]) -> httpx.Response:
        """
        Выполняет POST-запрос с обработкой ошибок и логированием.

        Args:
            url (str): URL endpoint для запроса
            token (str): JWT токен для авторизации в формате Bearer
            body_post (Dict[str, Any]): Тело запроса в формате JSON

        Returns:
            httpx.Response: Ответ от сервера

        Raises:
            Exception: Обернутая ошибка с понятным сообщением при сетевых проблемах


            >>> response = RequestModel.post("https://api.example.com/data", "token123", {"name": "test"})
        """
        try:
            return httpx.post(
                url=url,
                headers={"Authorization": f"Bearer {token}"},
                json=body_post,
                verify=False
            )
        except httpx.RequestError as e:
            logging.error(f"Произошла ошибка при выполнении POST-запроса: {e}")
            raise Exception("Ошибка выполнения POST-запроса") from e

    @staticmethod
    def patch(url: str, token: str, body_patch: Dict[str, Any]) -> httpx.Response:
        """
        Выполняет PATCH-запрос с обработкой ошибок и логированием.

        Args:
            url (str): URL endpoint для запроса
            token (str): JWT токен для авторизации в формате Bearer
            body_patch (Dict[str, Any]): Тело запроса для частичного обновления в формате JSON

        Returns:
            httpx.Response: Ответ от сервера

        Raises:
            Exception: Обернутая ошибка с понятным сообщением при сетевых проблемах



        """
        try:
            return httpx.patch(
                url=url,
                headers={"Authorization": f"Bearer {token}"},
                json=body_patch,
                verify=False
            )
        except httpx.RequestError as e:
            logging.error(f"Произошла ошибка при выполнении PATCH-запроса: {e}")
            raise Exception("Ошибка выполнения PATCH-запроса") from e

    @staticmethod
    def get(url: str, token: str) -> httpx.Response:
        """
        Выполняет GET-запрос с обработкой ошибок и логированием.

        Args:
            url (str): URL endpoint для запроса
            token (str): JWT токен для авторизации в формате Bearer

        Returns:
            httpx.Response: Ответ от сервера

        Raises:
            Exception: Обернутая ошибка с понятным сообщением при сетевых проблемах

        """
        try:
            return httpx.get(
                url=url,
                headers={"Authorization": f"Bearer {token}"},
                verify=False
            )
        except httpx.RequestError as e:
            logging.error(f"Произошла ошибка при выполнении GET-запроса: {e}")
            raise Exception("Ошибка выполнения GET-запроса") from e

    @staticmethod
    def delete(url: str, token: str) -> httpx.Response:
        """
        Выполняет DELETE-запрос с обработкой ошибок и логированием.

        Args:
            url (str): URL endpoint для запроса
            token (str): JWT токен для авторизации в формате Bearer

        Returns:
            httpx.Response: Ответ от сервера

        Raises:
            Exception: Обернутая ошибка с понятным сообщением при сетевых проблемах

        """
        try:
            return httpx.delete(
                url=url,
                headers={"Authorization": f"Bearer {token}"},
                verify=False
            )
        except httpx.RequestError as e:
            logging.error(f"Произошла ошибка при выполнении DELETE-запроса: {e}")
            raise Exception("Ошибка выполнения DELETE-запроса") from e