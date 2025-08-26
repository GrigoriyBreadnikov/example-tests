from smoke.api.vector.rest import VectorPost, VectorPatch, VectorGet, VectorDelete, VectorResponse
from smoke.api.vector.tests.assertions import VectorAssert
from smoke.api.vector.tests.faker import VectorFullData, VectorLength
from typing import Dict, Any, Optional, Union
import allure

# ШАГИ ДЛЯ ТЕСТОВ ВЕКТОРА



# Константы для шагов Allure
DATA_PREPARE_TITLE: str = "Подготовка тестовых данных"
POST_EXECUTE_TITLE: str = "Выполнение POST-запроса для создания вектора"
PATCH_EXECUTE_TITLE: str = "Выполнение PATCH-запроса для редактирования вектора"
GET_EXECUTE_TITLE: str = "Выполнение GET-запроса для получения вектора"
DELETE_EXECUTE_TITLE: str = "Выполнение DELETE-запроса для удаления вектора"
GET_PARAMS_TITLE: str = "Подготовка параметров запроса"

CHECK_201_TITLE: str = "Проверка кода ответа 201 (Created)"
CHECK_200_TITLE: str = "Проверка кода ответа 200 (OK)"
CHECK_204_TITLE: str = "Проверка кода ответа 204 (No Content)"
CHECK_400_TITLE: str = "Проверка кода ответа 400 (Bad Request)"
CHECK_409_TITLE: str = "Проверка кода ответа 409 (Conflict)"
CHECK_404_TITLE: str = "Проверка кода ответа 404 (Not Found)"

CHECK_DATA_RESPONSE_TITLE: str = "Проверка соответствия данных вектора в ответе"
CHECK_ID_LEN_TITLE: str = "Проверка длины ID вектора"
CHECK_NAME_TITLE: str = "Проверка соответствия имени"
CHECK_DESCRIPTION_TITLE: str = "Проверка соответствия описания"
CHECK_CONTENT_TITLE: str = "Проверка соответствия контента"
CHECK_CREATED_TIME_TITLE: str = "Проверка временной метки создания"
CHECK_UPDATED_TIME_TITLE: str = "Проверка временной метки обновления"
CHECK_DESCRIPTION_NULL_TITLE: str = "Проверка null-значения описания"

NULL_NAME_VECTOR_TITLE: str = "Проверка null-значения в поле name"
NULL_CONTENT_VECTOR_TITLE: str = "Проверка null-значения в поле content"
MESSAGE_INVALID_NAME_TITLE: str = "Проверка сообщения об ошибке для невалидного имени"
MESSAGE_INVALID_DESCRIPTION_TITLE: str = "Проверка сообщения об ошибке для невалидного описания"
MESSAGE_POST_DUBLICATE: str = "Проверка сообщения об ошибке дубликата"
MESSAGE_NOT_FOUND_TITLE: str = "Проверка сообщения об ошибке 'не найдено'"
MESSAGE_NULL_PAGE_OR_LIMIT_TITLE: str = "Проверка сообщения об ошибке для null page/limit"

DELETE_VECTOR_TITLE: str = "Удаление вектора после теста"
SEARCH_VALIDATION_TITLE: str = "Проверка результатов поиска"

# Инициализация клиентов
res = VectorResponse()
post = VectorPost()
patch = VectorPatch()
get = VectorGet()
delete = VectorDelete()
assertion = VectorAssert()
data = VectorFullData()

class StepsTestVector:
    """Класс для организации шагов тестирования Vector API"""

    # region Подготовка данных
    @staticmethod
    def data_prepare(name: Optional[str] = None,
                    description: Optional[str] = None,
                    content: Optional[str] = None) -> Dict[str, Any]:
        """Подготовка тестовых данных для тела вектора"""
        with allure.step(DATA_PREPARE_TITLE):
            if not any([name, description, content]):
                raise ValueError("Необходимо передать хотя бы один аргумент")

            print(f"\nТестовые данные: name={name}, description={description}, content={content}")
            return {
                "name": name,
                "description": description,
                "content": content
            }

    def data_prepare_full(self, random_name: str, random_description: str, random_content: str) -> Dict[str, Any]:
        """Подготовка полных тестовых данных"""
        return self.data_prepare(name=random_name, description=random_description, content=random_content)

    def data_prepare_without_name(self, random_description: str, random_content: str) -> Dict[str, Any]:
        """Подготовка данных без имени"""
        return self.data_prepare(description=random_description, content=random_content)

    def data_prepare_without_description(self, random_name: str, random_content: str) -> Dict[str, Any]:
        """Подготовка данных без описания"""
        return self.data_prepare(name=random_name, content=random_content)

    def data_prepare_without_content(self, random_name: str, random_description: str) -> Dict[str, Any]:
        """Подготовка данных без контента"""
        return self.data_prepare(name=random_name, description=random_description)

    @staticmethod
    def get_parameters_prepare(page: Optional[int] = None,
                              limit: Optional[int] = None,
                              q: Optional[str] = None) -> Dict[str, Any]:
        """Подготовка параметров запроса"""
        with allure.step(DATA_PREPARE_TITLE):
            if not any([page, limit, q]):
                raise ValueError("Необходимо передать хотя бы один аргумент")

            print(f"\nТестовые данные: page={page}, limit={limit}, q={q}")
            return {
                "page": page,
                "limit": limit,
                "q": q
            }
    # endregion

    # region Выполнение запросов
    @staticmethod
    def post_execute(token: str, name: Optional[str] = None,
                    description: Optional[str] = None,
                    content: Optional[str] = None) -> Any:
        """Выполнение POST-запроса для создания вектора"""
        with allure.step(POST_EXECUTE_TITLE):
            if not any([token, name, description, content]):
                raise ValueError("Необходимо передать хотя бы один аргумент")
            return res.get_response_vector(post.post_vector(token, name, description, content))

    def post_execute_full(self, token: str, name: str, description: str, content: str) -> Any:
        """Выполнение POST-запроса со всеми параметрами"""
        return self.post_execute(token, name=name, description=description, content=content)

    def post_execute_without_name(self, token: str, description: str, content: str) -> Any:
        """Выполнение POST-запроса без имени"""
        return self.post_execute(token, description=description, content=content)

    def post_execute_without_description(self, token: str, name: str, content: str) -> Any:
        """Выполнение POST-запроса без описания"""
        return self.post_execute(token, name=name, content=content)

    def post_execute_without_content(self, token: str, name: str, description: str) -> Any:
        """Выполнение POST-запроса без контента"""
        return self.post_execute(token, name=name, description=description)

    @staticmethod
    def patch_execute(token: str, id: str, name: Optional[str] = None,
                     description: Optional[str] = None,
                     content: Optional[str] = None) -> Any:
        """Выполнение PATCH-запроса для редактирования вектора"""
        with allure.step(PATCH_EXECUTE_TITLE):
            if not any([token, name, description, content]):
                raise ValueError("Необходимо передать хотя бы один аргумент")
            return res.get_response_vector(patch.patch_vector(token, id, name, description, content))

    def patch_execute_full(self, token: str, id: str, name: str, description: str, content: str) -> Any:
        """Выполнение PATCH-запроса со всеми параметрами"""
        return self.patch_execute(token, id, name=name, description=description, content=content)

    def patch_execute_without_name(self, token: str, id: str, description: str, content: str) -> Any:
        """Выполнение PATCH-запроса без имени"""
        return self.patch_execute(token, id, description=description, content=content)

    def patch_execute_without_description(self, token: str, id: str, name: str, content: str) -> Any:
        """Выполнение PATCH-запроса без описания"""
        return self.patch_execute(token, id, name=name, content=content)

    def patch_execute_without_content(self, token: str, id: str, name: str, description: str) -> Any:
        """Выполнение PATCH-запроса без контента"""
        return self.patch_execute(token, id, name=name, description=description)

    @staticmethod
    def get_execute(token: str) -> Any:
        """Выполнение GET-запроса для получения всех векторов"""
        with allure.step(GET_EXECUTE_TITLE):
            return res.get_response_vector(get.get_vector(token))

    @staticmethod
    def get_execute_page_limit_q(token: str, page: int, limit: int, q: str) -> Any:
        """Выполнение GET-запроса с параметрами пагинации и поиска"""
        with allure.step(GET_EXECUTE_TITLE):
            return res.get_response_vector(get.get_page_limit_q_vector(token, page, limit, q))

    @staticmethod
    def get_id_execute(token: str, id: str) -> Any:
        """Выполнение GET-запроса для получения вектора по ID"""
        with allure.step(GET_EXECUTE_TITLE):
            return res.get_response_vector(get.get_id_vector(token, id))

    @staticmethod
    def delete_execute(token: str, id: str) -> Any:
        """Выполнение DELETE-запроса для удаления вектора"""
        with allure.step(DELETE_EXECUTE_TITLE):
            return res.get_response_vector_code(delete.delete_vector(token, id))
    # endregion

    # region Проверки статус-кодов
    @staticmethod
    def check_status_201(response: Any) -> None:
        """Проверка кода ответа 201 (Created)"""
        with allure.step(CHECK_201_TITLE):
            assertion.post_success_201(response)

    @staticmethod
    def check_status_200(response: Any) -> None:
        """Проверка кода ответа 200 (OK) для PATCH"""
        with allure.step(CHECK_200_TITLE):
            assertion.patch_success_200(response)

    @staticmethod
    def check_get_status_200(response: Any) -> None:
        """Проверка кода ответа 200 (OK) для GET"""
        with allure.step(CHECK_200_TITLE):
            assertion.get_success_200(response)

    @staticmethod
    def check_status_204(response: Any) -> None:
        """Проверка кода ответа 204 (No Content)"""
        with allure.step(CHECK_204_TITLE):
            assertion.delete_success_204(response)

    @staticmethod
    def check_post_status_400(response: Any) -> None:
        """Проверка кода ответа 400 (Bad Request) для POST"""
        with allure.step(CHECK_400_TITLE):
            assertion.post_fail_400(response)

    @staticmethod
    def check_post_status_409(response: Any) -> None:
        """Проверка кода ответа 409 (Conflict) для POST"""
        with allure.step(CHECK_409_TITLE):
            assertion.post_dublicate_409(response)

    @staticmethod
    def check_patch_status_400(response: Any) -> None:
        """Проверка кода ответа 400 (Bad Request) для PATCH"""
        with allure.step(CHECK_400_TITLE):
            assertion.patch_fail_400(response)

    @staticmethod
    def check_get_status_400(response: Any) -> None:
        """Проверка кода ответа 400 (Bad Request) для GET"""
        with allure.step(CHECK_400_TITLE):
            assertion.get_fail_400(response)

    @staticmethod
    def check_patch_status_409(response: Any) -> None:
        """Проверка кода ответа 409 (Conflict) для PATCH"""
        with allure.step(CHECK_409_TITLE):
            assertion.patch_dublicate_409(response)
    # endregion

    # region Проверки данных ответа
    @staticmethod
    def check_response_id_len(response: Any) -> None:
        """Проверка длины ID вектора"""
        with allure.step(CHECK_ID_LEN_TITLE):
            assertion.post_id_len(response)

    @staticmethod
    def check_post_response_name(response: Any, name: str) -> None:
        """Проверка соответствия имени в POST-ответе"""
        with allure.step(CHECK_NAME_TITLE):
            assertion.post_assert_name(response, name)

    @staticmethod
    def check_post_response_description(response: Any, description: str) -> None:
        """Проверка соответствия описания в POST-ответе"""
        with allure.step(CHECK_DESCRIPTION_TITLE):
            assertion.post_assert_description(response, description)

    @staticmethod
    def check_post_response_content(response: Any, content: str) -> None:
        """Проверка соответствия контента в POST-ответе"""
        with allure.step(CHECK_CONTENT_TITLE):
            assertion.post_assert_content(response, content)

    @staticmethod
    def check_patch_response_id(response: Any, id: str) -> None:
        """Проверка соответствия ID в PATCH-ответе"""
        with allure.step(CHECK_NAME_TITLE):
            assertion.patch_id(response, id)

    @staticmethod
    def check_patch_response_name(response: Any, name: str) -> None:
        """Проверка соответствия имени в PATCH-ответе"""
        with allure.step(CHECK_NAME_TITLE):
            assertion.patch_assert_name(response, name)

    @staticmethod
    def check_patch_response_description(response: Any, description: str) -> None:
        """Проверка соответствия описания в PATCH-ответе"""
        with allure.step(CHECK_DESCRIPTION_TITLE):
            assertion.patch_assert_description(response, description)

    @staticmethod
    def check_patch_response_content(response: Any, content: str) -> None:
        """Проверка соответствия контента в PATCH-ответе"""
        with allure.step(CHECK_CONTENT_TITLE):
            assertion.patch_assert_content(response, content)

    @staticmethod
    def check_get_response_id(response: Any, id: str) -> None:
        """Проверка соответствия ID в GET-ответе"""
        with allure.step(CHECK_NAME_TITLE):
            assertion.get_id(response, id)

    @staticmethod
    def check_get_response_name(response: Any, name: str) -> None:
        """Проверка соответствия имени в GET-ответе"""
        with allure.step(CHECK_NAME_TITLE):
            assertion.get_assert_name(response, name)

    @staticmethod
    def check_get_response_description(response: Any, description: str) -> None:
        """Проверка соответствия описания в GET-ответе"""
        with allure.step(CHECK_DESCRIPTION_TITLE):
            assertion.get_assert_description(response, description)

    @staticmethod
    def check_get_response_content(response: Any, content: str) -> None:
        """Проверка соответствия контента в GET-ответе"""
        with allure.step(CHECK_CONTENT_TITLE):
            assertion.get_assert_content_special(response, content)

    @staticmethod
    def check_response_created_time(response: Any) -> None:
        """Проверка временной метки создания"""
        with allure.step(CHECK_CREATED_TIME_TITLE):
            assertion.created_time(response)

    @staticmethod
    def check_response_updated_time(response: Any) -> None:
        """Проверка временной метки обновления"""
        with allure.step(CHECK_UPDATED_TIME_TITLE):
            assertion.updated_time(response)

    @staticmethod
    def check_response_q_name(response: Any, q: str) -> None:
        """Проверка результатов поиска по имени"""
        with allure.step(SEARCH_VALIDATION_TITLE):
            assertion.response_q_name(response, q)

    @staticmethod
    def check_response_q_description(response: Any, q: str) -> None:
        """Проверка результатов поиска по описанию"""
        with allure.step(SEARCH_VALIDATION_TITLE):
            assertion.response_q_description(response, q)
    # endregion

    # region Проверки ошибок и специальных случаев
    @staticmethod
    def check_post_message_name_null(response: Any) -> None:
        """Проверка сообщения об ошибке для null-имени в POST"""
        with allure.step(NULL_NAME_VECTOR_TITLE):
            assertion.post_message_name_null(response)

    @staticmethod
    def check_post_message_content_null(response: Any) -> None:
        """Проверка сообщения об ошибке для null-контента в POST"""
        with allure.step(NULL_CONTENT_VECTOR_TITLE):
            assertion.post_message_content_null(response)

    @staticmethod
    def check_post_message_name_invalid(response: Any) -> None:
        """Проверка сообщения об ошибке для невалидного имени в POST"""
        with allure.step(MESSAGE_INVALID_NAME_TITLE):
            assertion.post_message_name_invalid(response)

    @staticmethod
    def check_post_message_description_invalid(response: Any) -> None:
        """Проверка сообщения об ошибке для невалидного описания в POST"""
        with allure.step(MESSAGE_INVALID_DESCRIPTION_TITLE):
            assertion.post_message_description_invalid(response)

    @staticmethod
    def check_post_response_description_null(response: Any) -> None:
        """Проверка null-значения описания в POST-ответе"""
        with allure.step(CHECK_DESCRIPTION_NULL_TITLE):
            assertion.post_description_null(response)

    @staticmethod
    def check_patch_response_description_null(response: Any) -> None:
        """Проверка null-значения описания в PATCH-ответе"""
        with allure.step(CHECK_DESCRIPTION_NULL_TITLE):
            assertion.patch_description_null(response)

    @staticmethod
    def check_post_message_dublicate(response: Any) -> None:
        """Проверка сообщения об ошибке дубликата в POST"""
        with allure.step(MESSAGE_POST_DUBLICATE):
            assertion.post_message_dublicate(response)

    @staticmethod
    def check_patch_message_name_null(response: Any) -> None:
        """Проверка сообщения об ошибке для null-имени в PATCH"""
        with allure.step(NULL_NAME_VECTOR_TITLE):
            assertion.patch_message_name_null(response)

    @staticmethod
    def check_patch_message_content_null(response: Any) -> None:
        """Проверка сообщения об ошибке для null-контента в PATCH"""
        with allure.step(NULL_CONTENT_VECTOR_TITLE):
            assertion.patch_message_content_null(response)

    @staticmethod
    def check_patch_message_name_invalid(response: Any) -> None:
        """Проверка сообщения об ошибке для невалидного имени в PATCH"""
        with allure.step(MESSAGE_INVALID_NAME_TITLE):
            assertion.patch_message_name_invalid(response)

    @staticmethod
    def check_patch_message_description_invalid(response: Any) -> None:
        """Проверка сообщения об ошибке для невалидного описания в PATCH"""
        with allure.step(MESSAGE_INVALID_DESCRIPTION_TITLE):
            assertion.patch_message_description_invalid(response)

    @staticmethod
    def check_patch_message_dublicate(response: Any) -> None:
        """Проверка сообщения об ошибке дубликата в PATCH"""
        with allure.step(MESSAGE_POST_DUBLICATE):
            assertion.patch_message_dublicate(response)

    @staticmethod
    def check_message_not_found(response: Any) -> None:
        """Проверка сообщения об ошибке 'не найдено'"""
        with allure.step(MESSAGE_NOT_FOUND_TITLE):
            assertion.message_not_found(response)

    @staticmethod
    def check_message_null_page_or_limit(response: Any) -> None:
        """Проверка сообщения об ошибке для null page/limit"""
        with allure.step(MESSAGE_NULL_PAGE_OR_LIMIT_TITLE):
            assertion.message_null_page_or_limit(response)
    # endregion

    # region Утилиты
    @staticmethod
    def clean_env(token: str, response: Any) -> None:
        """Очистка тестового окружения - удаление вектора"""
        with allure.step(DELETE_VECTOR_TITLE):
            delete.delete_vector(token, response['response']['id'])

    # endregion



    def yy(self):
        ttt = ['f', 'a', 'b']
        tt = sorted(ttt)
        print(tt)

ii = StepsTestVector()
ii.yy()