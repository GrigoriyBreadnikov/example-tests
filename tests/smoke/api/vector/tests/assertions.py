"""
Модуль VectorAssert предоставляет набор утверждений (assertions) для тестирования API работы с векторами.

Содержит методы для проверки:
- Кодов состояния HTTP (200, 201, 204, 400, 404, 409)
- Тела ответа (параметры name, description, content)
- Сообщений об ошибках
- Временных меток (created_time, updated_time)
- Идентификаторов
"""

from typing import Dict, Any, Optional

from smoke.api.main import GeneralFunctions
from smoke.api.assertion_main import (
    StatusCodeAssert,
    BodyParameterAssert,
    MessageAssert,
    EndpointName
)

# Инициализация вспомогательных классов
GF: GeneralFunctions = GeneralFunctions()  # Общие функции
SCA: StatusCodeAssert = StatusCodeAssert()  # Проверка кодов состояния
BPA: BodyParameterAssert = BodyParameterAssert()  # Проверка параметров тела ответа
MA: MessageAssert = MessageAssert()  # Проверка сообщений
EN: EndpointName = EndpointName()  # Формирование имен конечных точек

# Константы для работы с векторами
VECTOR: str = "vector"
VECTOR_POST_NAME: str = EN.endpoint_post(VECTOR)  # Имя endpoint для POST
VECTOR_PATCH_NAME: str = EN.endpoint_patch(VECTOR)  # Имя endpoint для PATCH
VECTOR_GET_NAME: str = EN.endpoint_get(VECTOR)  # Имя endpoint для GET
VECTOR_DELETE_NAME: str = EN.endpoint_delete(VECTOR)  # Имя endpoint для DELETE

# Сообщения об ошибках
VECTOR_MESSAGE_NAME_NULL: str = "неверное тело запроса: name: не может быть пустым."
VECTOR_MESSAGE_CONTENT_NULL: str = "неверное тело запроса: content: не может быть пустым."
VECTOR_MESSAGE_NAME_INVALID: str = ("неверное тело запроса: name: должно содержать только разрешенные символы (латинские буквы, цифры,  точки, дефисы и подчеркивания) "
                                    "и содержать не более 100 символов.")
VECTOR_MESSAGE_DESCRIPTION_INVALID: str = ("неверное тело запроса: description: должно содержать только разрешенные символы "
                                           "(буквы, цифры, пробелы и специальные символы) и содержать не более 500 символов.")
VECTOR_MESSAGE_DUBLICATE: str = "конфигурация вектора уже существует"
VECTOR_MESSAGE_NOT_FOUND: str = "сущность не найдена"
VECTOR_MESSAGE_NULL_PAGE_OR_LIMIT: str = "недопустимый запроса"


class VectorAssert:
    """
    Класс с утверждениями для тестирования API векторов.
    Все методы статические или экземплярные для удобства использования в тестах.
    """

    # region Проверки кодов состояния

    @staticmethod
    def patch_success_200(response: Dict[str, Any]) -> None:
        """Проверяет успешный PATCH-запрос (код 200)"""
        SCA.assert_200(response, VECTOR_PATCH_NAME)

    @staticmethod
    def get_success_200(response: Dict[str, Any]) -> None:
        """Проверяет успешный GET-запрос (код 200)"""
        SCA.assert_200(response, VECTOR_GET_NAME)

    @staticmethod
    def post_success_201(response: Dict[str, Any]) -> None:
        """Проверяет успешный POST-запрос (код 201)"""
        SCA.assert_201(response, VECTOR_POST_NAME)

    @staticmethod
    def delete_success_204(status_code: int) -> None:
        """
        Проверяет успешный DELETE-запрос (код 204)

        Args:
            status_code: Числовой HTTP статус-код ответа

        Raises:
            AssertionError: Если статус-код не равен 204
        """
        assert status_code == 204, f"{VECTOR_DELETE_NAME} вернул не 204 код, а {status_code}"

    @staticmethod
    def dublicate(response: Dict[str, Any], endpoint_name: str) -> None:
        """Проверяет конфликт при дублировании (код 409)"""
        SCA.assert_409(response, endpoint_name)

    def post_dublicate_409(self, response: Dict[str, Any]) -> None:
        """Проверяет конфликт при дублировании в POST (код 409)"""
        self.dublicate(response, VECTOR_POST_NAME)

    def patch_dublicate_409(self, response: Dict[str, Any]) -> None:
        """Проверяет конфликт при дублировании в PATCH (код 409)"""
        self.dublicate(response, VECTOR_PATCH_NAME)

    @staticmethod
    def fail(response: Dict[str, Any], endpoint_name: str) -> None:
        """Проверяет некорректный запрос (код 400)"""
        SCA.assert_400(response, endpoint_name)

    def post_fail_400(self, response: Dict[str, Any]) -> None:
        """Проверяет некорректный POST-запрос (код 400)"""
        self.fail(response, VECTOR_POST_NAME)

    def patch_fail_400(self, response: Dict[str, Any]) -> None:
        """Проверяет некорректный PATCH-запрос (код 400)"""
        self.fail(response, VECTOR_PATCH_NAME)
    def get_fail_400(self, response: Dict[str, Any]) -> None:
        """Проверяет некорректный GET-запрос (код 400)"""
        self.fail(response, VECTOR_GET_NAME)
    @staticmethod
    def not_found_404(response: Dict[str, Any]) -> None:
        """Проверяет отсутствие сущности (код 404)"""
        SCA.assert_404(response, VECTOR_GET_NAME)

    # endregion

    # region Проверки содержимого ответа

    @staticmethod
    def response_content(response: Dict[str, Any], content: str) -> None:
        """Проверяет наличие указанного контента в ответе"""
        assert GF.contains_all(response["response"]["content"], f"vectorConfig:\n  {content}")

    @staticmethod
    def assert_name(response: Dict[str, Any], variable: str, endpoint_name: str) -> None:
        """Проверяет параметр name в ответе"""
        BPA.assert_response_parameter(response, "name", variable, endpoint_name)

    def post_assert_name(self, response: Dict[str, Any], variable: str) -> None:
        """Проверяет параметр name для POST-запроса"""
        self.assert_name(response, variable, VECTOR_POST_NAME)

    def patch_assert_name(self, response: Dict[str, Any], variable: str) -> None:
        """Проверяет параметр name для PATCH-запроса"""
        self.assert_name(response, variable, VECTOR_PATCH_NAME)

    def get_assert_name(self, response: Dict[str, Any], variable: str) -> None:
        """Проверяет параметр name для GET-запроса"""
        self.assert_name(response, variable, VECTOR_GET_NAME)

    @staticmethod
    def assert_description(response: Dict[str, Any], variable: Optional[str], endpoint_name: str) -> None:
        """Проверяет параметр description в ответе"""
        BPA.assert_response_parameter(response, "description", variable, endpoint_name)

    def post_assert_description(self, response: Dict[str, Any], variable: Optional[str]) -> None:
        """Проверяет параметр description для POST-запроса"""
        self.assert_description(response, variable, VECTOR_POST_NAME)

    def patch_assert_description(self, response: Dict[str, Any], variable: Optional[str]) -> None:
        """Проверяет параметр description для PATCH-запроса"""
        self.assert_description(response, variable, VECTOR_PATCH_NAME)

    def get_assert_description(self, response: Dict[str, Any], variable: Optional[str]) -> None:
        """Проверяет параметр description для GET-запроса"""
        self.assert_description(response, variable, VECTOR_GET_NAME)

    @staticmethod
    def assert_content(response: Dict[str, Any], content: str, endpoint_name: str) -> None:
        """Проверяет параметр content в ответе"""
        assert GF.contains_all(response["response"]["content"], f"vectorConfig:\n  {content}"), \
            f"{endpoint_name} вернул content не из запроса"

    @staticmethod
    def assert_content_get_id(response: Dict[str, Any], content: str, endpoint_name: str) -> None:
        """Проверяет параметр content в ответе"""
        assert GF.contains_all(f"vectorConfig:\n  {content}", response["response"]["content"]), \
            f"{endpoint_name} вернул content не из запроса"

    def post_assert_content(self, response: Dict[str, Any], variable: str) -> None:
        """Проверяет параметр content для POST-запроса"""
        self.assert_content(response, variable, VECTOR_POST_NAME)

    def patch_assert_content(self, response: Dict[str, Any], variable: str) -> None:
        """Проверяет параметр content для PATCH-запроса"""
        self.assert_content(response, variable, VECTOR_PATCH_NAME)

    def get_assert_content(self, response: Dict[str, Any], variable: str) -> None:
        """Проверяет параметр content для GET-запроса"""
        self.assert_content(response, variable, VECTOR_GET_NAME)

    def get_assert_content_special(self, response: Dict[str, Any], variable: str) -> None:
        """Проверяет параметр content для GET-запроса c id"""
        self.assert_content_get_id(response, variable, VECTOR_GET_NAME)
    # endregion

    # region Проверки идентификаторов и временных меток

    @staticmethod
    def id_len(response: Dict[str, Any], endpoint_name: str) -> None:
        """Проверяет длину ID (16 символов)"""
        BPA.assert_id_len(response, 16, endpoint_name)

    def post_id_len(self, response: Dict[str, Any]) -> None:
        """Проверяет длину ID для POST-запроса"""
        self.id_len(response, VECTOR_POST_NAME)

    def patch_id_len(self, response: Dict[str, Any]) -> None:
        """Проверяет длину ID для PATCH-запроса"""
        self.id_len(response, VECTOR_PATCH_NAME)

    @staticmethod
    def created_time(response: Dict[str, Any]) -> None:
        """Проверяет временную метку создания"""
        BPA.assert_created_time(response, VECTOR_POST_NAME)

    @staticmethod
    def updated_time(response: Dict[str, Any]) -> None:
        """Проверяет временную метку обновления"""
        BPA.assert_updated_time(response, VECTOR_PATCH_NAME)

    @staticmethod
    def description_null(response: Dict[str, Any], endpoint_name: str) -> None:
        """Проверяет отсутствие description в ответе"""
        BPA.assert_not_in(response, "description", endpoint_name)

    def post_description_null(self, response: Dict[str, Any]) -> None:
        """Проверяет отсутствие description для POST-запроса"""
        self.description_null(response, VECTOR_POST_NAME)

    def patch_description_null(self, response: Dict[str, Any]) -> None:
        """Проверяет отсутствие description для PATCH-запроса"""
        self.description_null(response, VECTOR_PATCH_NAME)

    @staticmethod
    def id_equal(response: Dict[str, Any], id: str, endpoint_name: str) -> None:
        """Проверяет соответствие ID"""
        BPA.assert_id(response, id, endpoint_name)

    def patch_id(self, response: Dict[str, Any], id: str) -> None:
        """Проверяет ID для PATCH-запроса"""
        self.id_equal(response, id, VECTOR_PATCH_NAME)

    def get_id(self, response: Dict[str, Any], id: str) -> None:
        """Проверяет ID для GET-запроса"""
        self.id_equal(response, id, VECTOR_GET_NAME)


    @staticmethod
    def response_q_name(response: Dict[str, Any], name: str) -> None:
        """Проверяет наличие указанного name в ответе после поиска"""
        assert response["response"]["vectors"][0]["name"] == name, f"{VECTOR_GET_NAME} вернул name не из поискового запроса"

    @staticmethod
    def response_q_description(response: Dict[str, Any], description: str) -> None:
        """Проверяет наличие указанного description в ответе после поиска"""
        assert response["response"]["vectors"][0]["description"] == description, f"{VECTOR_GET_NAME} вернул description не из поискового запроса"

    # endregion

    # region Проверки сообщений об ошибках

    @staticmethod
    def message_name_null(response: Dict[str, Any], endpoint_name: str) -> None:
        """Проверяет сообщение об ошибке пустого name"""
        MA.message_response(response, VECTOR_MESSAGE_NAME_NULL, endpoint_name)

    def post_message_name_null(self, response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке пустого name для POST"""
        self.message_name_null(response, VECTOR_POST_NAME)

    def patch_message_name_null(self, response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке пустого name для PATCH"""
        self.message_name_null(response, VECTOR_PATCH_NAME)

    @staticmethod
    def message_content_null(response: Dict[str, Any], endpoint_name: str) -> None:
        """Проверяет сообщение об ошибке пустого content"""
        MA.message_response(response, VECTOR_MESSAGE_CONTENT_NULL, endpoint_name)

    def post_message_content_null(self, response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке пустого content для POST"""
        self.message_content_null(response, VECTOR_POST_NAME)

    def patch_message_content_null(self, response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке пустого content для PATCH"""
        self.message_content_null(response, VECTOR_PATCH_NAME)

    @staticmethod
    def message_name_invalid(response: Dict[str, Any], endpoint_name: str) -> None:
        """Проверяет сообщение об ошибке невалидного name"""
        MA.message_response(response, VECTOR_MESSAGE_NAME_INVALID, endpoint_name)

    def post_message_name_invalid(self, response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке невалидного name для POST"""
        self.message_name_invalid(response, VECTOR_POST_NAME)

    def patch_message_name_invalid(self, response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке невалидного name для PATCH"""
        self.message_name_invalid(response, VECTOR_PATCH_NAME)

    @staticmethod
    def message_description_invalid(response: Dict[str, Any], endpoint_name: str) -> None:
        """Проверяет сообщение об ошибке невалидного description"""
        MA.message_response(response, VECTOR_MESSAGE_DESCRIPTION_INVALID, endpoint_name)

    def post_message_description_invalid(self, response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке невалидного description для POST"""
        self.message_description_invalid(response, VECTOR_POST_NAME)

    def patch_message_description_invalid(self, response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке невалидного description для PATCH"""
        self.message_description_invalid(response, VECTOR_PATCH_NAME)

    @staticmethod
    def message_dublicate(response: Dict[str, Any], endpoint_name: str) -> None:
        """Проверяет сообщение об ошибке дублирования"""
        MA.message_response(response, VECTOR_MESSAGE_DUBLICATE, endpoint_name)

    def post_message_dublicate(self, response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке дублирования для POST"""
        self.message_dublicate(response, VECTOR_POST_NAME)

    def patch_message_dublicate(self, response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке дублирования для PATCH"""
        self.message_dublicate(response, VECTOR_PATCH_NAME)

    @staticmethod
    def message_not_found(response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке отсутствия сущности"""
        MA.message_response(response, VECTOR_MESSAGE_NOT_FOUND, VECTOR_GET_NAME)

    @staticmethod
    def message_null_page_or_limit(response: Dict[str, Any]) -> None:
        """Проверяет сообщение об ошибке при пустых параметрах page или limit"""
        MA.message_response(response, VECTOR_MESSAGE_NULL_PAGE_OR_LIMIT, VECTOR_GET_NAME)

    # endregion