import allure
import json
from typing import Any, Dict, Union
import requests

STATUS_CODE: Dict[str, int] = {
    "200": 200,  # OK - успешный запрос
    "201": 201,  # Created - ресурс создан
    "204": 204,  # No Content - успешно, но нет содержимого
    "400": 400,  # Bad Request - неверный запрос
    "404": 404,  # Not Found - ресурс не найден
    "409": 409,  # Conflict - конфликт данных (дубликат)
    "500": 500   # Internal Server Error - внутренняя ошибка сервера
}

class ResponseModel:
    """
    Класс для обработки и документирования HTTP-ответов в Allure-отчетах.
    Предоставляет методы для извлечения и оформления данных из ответов API.
    """

    @staticmethod
    def response_body(method: str, part_response: str) -> str:
        """
        Формирует строку для описания части ответа в отчетах.

        Args:
            method: HTTP-метод (GET, POST, etc.)
            part_response: Название части ответа

        Returns:
            str: Отформатированная строка вида "method.part_response"

        """
        return f"{method}.{part_response}"

    @staticmethod
    def response_status_code(method: requests.Response) -> int:
        """
        Извлекает статус-код из HTTP-ответа.

        Args:
            method: Объект ответа requests.Response

        Returns:
            int: HTTP статус-код

        """
        return method.status_code

    @staticmethod
    def response_body_or_message(method: requests.Response) -> Union[Dict[str, Any], str]:
        """
        Извлекает JSON-тело ответа или текстовое сообщение при ошибке.

        Args:
            method: Объект ответа requests.Response

        Returns:
            Union[Dict[str, Any], str]: JSON-данные или текстовое сообщение

        Raises:
            JSONDecodeError: Если ответ не является валидным JSON
        """
        try:
            return method.json()
        except json.JSONDecodeError:
            return method.text

    def response_all(self, method: requests.Response) -> Dict[str, Any]:
        """
        Обрабатывает полный HTTP-ответ и прикрепляет данные к Allure-отчету.

        Args:
            method: Объект ответа requests.Response

        Returns:
            Dict[str, Any]: Словарь с статус-кодом и телом ответа


            {'status_code': 200, 'response': {'data': 'value'}}
        """
        status_code = self.response_status_code(method)
        body_or_message = self.response_body_or_message(method)

        response_body = {
            "status_code": status_code,
            "response": body_or_message
        }

        try:
            # Автоматическое прикрепление ответа к Allure-отчету
            with allure.step("API Response"):
                allure.attach(
                    json.dumps(response_body, indent=2, ensure_ascii=False),
                    name="Response Data",
                    attachment_type=allure.attachment_type.JSON
                )
        except Exception:
            # Игнорируем ошибки прикрепления чтобы не ломать тесты
            pass

        return response_body