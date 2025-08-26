from typing import Any, Dict
from smoke.api.models.response import STATUS_CODE
from smoke.api.main import GeneralFunctions

GF = GeneralFunctions()


class StatusCodeAssert:
    """
    Класс для проверки HTTP статус-кодов в ответах API.

    Предоставляет методы для проверки стандартных статус-кодов (200, 201, 400 и т.д.)
    с понятными сообщениями об ошибках.
    """

    @staticmethod
    def assert_status_code(response: Dict[str, Any], status_code: int, title_message_assert: str) -> None:
        """
        Проверяет соответствие статус-кода в ответе ожидаемому значению.

        Args:
            response: Ответ API, содержащий ключ 'status_code'
            status_code: Ожидаемый HTTP статус-код
            title_message_assert: Описание проверки для сообщения об ошибке

        Raises:
            AssertionError: Если статус-код не соответствует ожидаемому
        """
        assert response["status_code"] == status_code, f"{title_message_assert} вернул не {status_code} код"

    @staticmethod
    def delete_status_code(response: int, status_code: int, title_message_assert: str) -> None:
        """
        Специальная проверка для DELETE запросов, где ответ может быть просто статус-кодом.

        Args:
            response: Полученный статус-код
            status_code: Ожидаемый статус-код
            title_message_assert: Описание проверки для сообщения об ошибке

        Raises:
            AssertionError: Если статус-код не соответствует ожидаемому
        """
        assert response == status_code, f"{title_message_assert} вернул не {status_code} код, а "

    def assert_200(self, response: Dict[str, Any], title_message_assert: str) -> None:
        """Проверяет успешный статус 200 OK"""
        self.assert_status_code(response, STATUS_CODE["200"], title_message_assert)

    def assert_201(self, response: Dict[str, Any], title_message_assert: str) -> None:
        """Проверяет статус 201 Created"""
        self.assert_status_code(response, STATUS_CODE["201"], title_message_assert)

    def assert_204(self, response: Dict[str, Any], title_message_assert: str) -> None:
        """Проверяет статус 204 No Content"""
        self.assert_status_code(response, STATUS_CODE["204"], title_message_assert)

    def assert_400(self, response: Dict[str, Any], title_message_assert: str) -> None:
        """Проверяет ошибку 400 Bad Request"""
        self.assert_status_code(response, STATUS_CODE["400"], title_message_assert)

    def assert_404(self, response: Dict[str, Any], title_message_assert: str) -> None:
        """Проверяет ошибку 404 Not Found"""
        self.assert_status_code(response, STATUS_CODE["404"], title_message_assert)

    def assert_409(self, response: Dict[str, Any], title_message_assert: str) -> None:
        """Проверяет ошибку 409 Conflict"""
        self.assert_status_code(response, STATUS_CODE["409"], title_message_assert)

    def assert_500(self, response: Dict[str, Any], title_message_assert: str) -> None:
        """Проверяет ошибку 500 Internal Server Error"""
        self.assert_status_code(response, STATUS_CODE["500"], title_message_assert)


class BodyParameterAssert:
    """
    Класс для проверки параметров тела ответа API.

    Содержит методы для проверки:
    - Соответствия параметров
    - Длины ID
    - Временных меток
    - Отсутствия параметров
    """

    @staticmethod
    def assert_response_parameter(response: Dict[str, Any], parameter: str, variable: Any, endpoint_name: str) -> None:
        """
        Проверяет соответствие параметра в ответе ожидаемому значению.

        Args:
            response: Ответ API
            parameter: Название проверяемого параметра
            variable: Ожидаемое значение параметра
            endpoint_name: Название эндпоинта для сообщения об ошибке

        Raises:
            AssertionError: Если параметр не соответствует ожидаемому значению
        """
        assert response["response"][parameter] == variable, f"{endpoint_name} вернул {parameter} не из запроса"



    @staticmethod
    def assert_id_len(response: Dict[str, Any], length: int, endpoint_name: str) -> None:
        """
        Проверяет длину ID в ответе.

        Args:
            response: Ответ API
            length: Ожидаемая длина ID
            endpoint_name: Название эндпоинта для сообщения об ошибке

        Raises:
            AssertionError: Если длина ID не соответствует ожидаемой
        """
        assert len(response["response"]["id"]) == length, f"{endpoint_name} вернул id невалидный по длине"

    def assert_id(self, response: Dict[str, Any], id: str, endpoint_name: str) -> None:
        """Проверяет соответствие ID"""
        self.assert_response_parameter(response, "id", id, f"{endpoint_name} вернул id невалидный по длине")

    def assert_created_time(self, response: Dict[str, Any], endpoint_name: str) -> None:
        """
        Проверяет, что created_time содержит текущее время.

        Args:
            response: Ответ API
            endpoint_name: Название эндпоинта для сообщения об ошибке
        """
        assert GF.now_time() in response["response"]["created_time"], f"{endpoint_name} вернул не текущий created_time"

    def assert_updated_time(self, response: Dict[str, Any], endpoint_name: str) -> None:
        """
        Проверяет, что updated_time содержит текущее время.

        Args:
            response: Ответ API
            endpoint_name: Название эндпоинта для сообщения об ошибке
        """
        assert GF.now_time() in response["response"]["updated_time"], f"{endpoint_name} вернул не текущий created_time"

    def assert_not_in(self, response: Dict[str, Any], parameter: str, endpoint_name: str) -> None:
        """
        Проверяет отсутствие параметра в ответе.

        Args:
            response: Ответ API
            parameter: Название параметра, который должен отсутствовать
            endpoint_name: Название эндпоинта для сообщения об ошибке
        """
        assert parameter not in response, f"{endpoint_name} присутствует в ответе"


class MessageAssert:
    """
    Класс для проверки текстовых сообщений в ответах API.
    """

    @staticmethod
    def message_response(response: Dict[str, Any], message: str, endpoint_name: str) -> None:
        """
        Проверяет соответствие текста сообщения в ответе ожидаемому.

        Args:
            response: Ответ API
            message: Ожидаемый текст сообщения
            endpoint_name: Название эндпоинта для сообщения об ошибке

        Raises:
            AssertionError: Если текст сообщения не соответствует ожидаемому
        """
        assert response["response"]["message"] == message, f"{endpoint_name} вернул неправильный текст ответа"


class EndpointName:
    """
    Класс для генерации стандартизированных названий эндпоинтов.

    Используется для формирования единообразных сообщений в тестах.
    """

    @staticmethod
    def endpoint(method: str, name_route: str) -> str:
        """
        Формирует название эндпоинта по методу и пути.

        Args:
            method: HTTP метод (GET, POST и т.д.)
            name_route: Путь эндпоинта

        Returns:
            Строка в формате "Эндпоинт {method} /{name_route}"
        """
        return f"Эндпоинт {method} /{name_route}"

    def endpoint_post(self, name_route: str) -> str:
        """Генерирует название для POST эндпоинта"""
        return self.endpoint("POST", name_route)

    def endpoint_patch(self, name_route: str) -> str:
        """Генерирует название для PATCH эндпоинта"""
        return self.endpoint("PATCH", name_route)

    def endpoint_put(self, name_route: str) -> str:
        """Генерирует название для PUT эндпоинта"""
        return self.endpoint("PUT", name_route)

    def endpoint_get(self, name_route: str) -> str:
        """Генерирует название для GET эндпоинта"""
        return self.endpoint("GET", name_route)

    def endpoint_delete(self, name_route: str) -> str:
        """Генерирует название для DELETE эндпоинта"""
        return self.endpoint("DELETE", name_route)