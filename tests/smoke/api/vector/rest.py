from typing import Dict, Any
from smoke.api.config import env
from smoke.api.models.request import RequestModel
from smoke.api.models.response import ResponseModel

# Инициализация объектов для работы с запросами и ответами
Req: RequestModel = RequestModel()
Res: ResponseModel = ResponseModel()


class VectorRequestBody:
    """
    Класс для формирования тел запросов API для работы с векторами.

    Содержит методы для создания тел запросов с различными комбинациями параметров.
    """

    @staticmethod
    def vector_body(name: str, description: str, content: str) -> Dict[str, str]:
        """
        Формирует тело запроса со всеми параметрами.

        Args:
            name: Название вектора
            description: Описание вектора
            content: Содержимое вектора

        Returns:
            Словарь с полным телом запроса
        """
        return {
            "name": name,
            "description": description,
            "content": content
        }

    @staticmethod
    def vector_body_without_name(description: str, content: str) -> Dict[str, str]:
        """
        Формирует тело запроса без параметра name.

        Args:
            description: Описание вектора
            content: Содержимое вектора

        Returns:
            Словарь с телом запроса без name
        """
        return {
            "description": description,
            "content": content
        }

    @staticmethod
    def vector_body_without_description(name: str, content: str) -> Dict[str, str]:
        """
        Формирует тело запроса без параметра description.

        Args:
            name: Название вектора
            content: Содержимое вектора

        Returns:
            Словарь с телом запроса без description
        """
        return {
            "name": name,
            "content": content
        }

    @staticmethod
    def vector_body_without_content(name: str, description: str) -> Dict[str, str]:
        """
        Формирует тело запроса без параметра content.

        Args:
            name: Название вектора
            description: Описание вектора

        Returns:
            Словарь с телом запроса без content
        """
        return {
            "name": name,
            "description": description
        }

    @staticmethod
    def url_id(id: str) -> str:
        """
        Формирует URL для работы с конкретным вектором по ID.

        Args:
            id: Идентификатор вектора

        Returns:
            Полный URL вида {BASE_URL}/{id}
        """
        return f"{env.VECTOR_URL}/{id}"

    @staticmethod
    def url_page_limit_q(page: int, limit: int, q: str) -> str:
        """
        Формирует URL для пагинации списка векторов с указанием лимита на странице.

        Args:
            limit: Количество векторов на одной странице (максимальное значение зависит от API)
                   Пример: 10, 25, 50, 100

        Returns:
            str: Полный URL вида {BASE_URL}/vectors?page=1&limit={limit}

        Notes:
            - Страница всегда устанавливается на 1 (первая страница)
            - Лимит должен быть положительным целым числом
            - Максимальное значение лимита определяется API
        """
        return f"{env.VECTOR_URL}?page={page}&limit={limit}&q=group_id%3D1%5Ename%20contain%20{q}%5ENFORdescription%20contain%20{q}&page=1&limit=20"


class VectorPost(VectorRequestBody):
    """
    Класс для выполнения POST-запросов к API векторов.
    Наследует методы формирования тел запросов от VectorRequestBody.
    """

    def post_vector(self, token: str, name: str, description: str, content: str) -> Any:
        """
        Отправляет POST-запрос для создания вектора со всеми параметрами.

        Args:
            token: Токен авторизации
            name: Название вектора
            description: Описание вектора
            content: Содержимое вектора

        Returns:
            Ответ от API
        """
        return Req.post(env.VECTOR_URL, token, self.vector_body(name, description, content))

    def post_vector_without_name(self, token: str, description: str, content: str) -> Any:
        """
        Отправляет POST-запрос без параметра name.

        Args:
            token: Токен авторизации
            description: Описание вектора
            content: Содержимое вектора

        Returns:
            Ответ от API
        """
        return Req.post(env.VECTOR_URL, token, self.vector_body_without_name(description, content))

    def post_vector_without_description(self, token: str, name: str, content: str) -> Any:
        """
        Отправляет POST-запрос без параметра description.

        Args:
            token: Токен авторизации
            name: Название вектора
            content: Содержимое вектора

        Returns:
            Ответ от API
        """
        return Req.post(env.VECTOR_URL, token, self.vector_body_without_description(name, content))

    def post_vector_without_content(self, token: str, name: str, description: str) -> Any:
        """
        Отправляет POST-запрос без параметра content.

        Args:
            token: Токен авторизации
            name: Название вектора
            description: Описание вектора

        Returns:
            Ответ от API
        """
        return Req.post(env.VECTOR_URL, token, self.vector_body_without_content(name, description))

    @staticmethod
    def vector_execute_post_full_body(token: str, body: Dict[str, Any]) -> Any:
        """
        Отправляет POST-запрос с полным пользовательским телом запроса.

        Args:
            token: Токен авторизации
            body: Полное тело запроса

        Returns:
            Ответ от API
        """
        return Req.post(env.VECTOR_URL, token, body)


class VectorPatch(VectorRequestBody):
    """
    Класс для выполнения PATCH-запросов к API векторов.
    Наследует методы формирования тел запросов от VectorRequestBody.
    """

    def patch_vector(self, token: str, id: str, name: str, description: str, content: str) -> Any:
        """
        Отправляет PATCH-запрос для обновления вектора со всеми параметрами.

        Args:
            token: Токен авторизации
            id: Идентификатор вектора
            name: Название вектора
            description: Описание вектора
            content: Содержимое вектора

        Returns:
            Ответ от API
        """
        return Req.patch(self.url_id(id), token, self.vector_body(name, description, content))

    def patch_vector_without_name(self, token: str, id: str, description: str, content: str) -> Any:
        """
        Отправляет PATCH-запрос без параметра name.

        Args:
            token: Токен авторизации
            id: Идентификатор вектора
            description: Описание вектора
            content: Содержимое вектора

        Returns:
            Ответ от API
        """
        return Req.patch(self.url_id(id), token, self.vector_body_without_name(description, content))

    def patch_vector_without_description(self, token: str, id: str, name: str, content: str) -> Any:
        """
        Отправляет PATCH-запрос без параметра description.

        Args:
            token: Токен авторизации
            id: Идентификатор вектора
            name: Название вектора
            content: Содержимое вектора

        Returns:
            Ответ от API
        """
        return Req.patch(self.url_id(id), token, self.vector_body_without_description(name, content))

    def patch_vector_without_content(self, token: str, id: str, name: str, description: str) -> Any:
        """
        Отправляет PATCH-запрос без параметра content.

        Args:
            token: Токен авторизации
            id: Идентификатор вектора
            name: Название вектора
            description: Описание вектора

        Returns:
            Ответ от API
        """
        return Req.patch(self.url_id(id), token, self.vector_body_without_content(name, description))

    def patch_vector_full_body(self, token: str, id: str, body: Dict[str, Any]) -> Any:
        """
        Отправляет PATCH-запрос с полным пользовательским телом запроса.

        Args:
            token: Токен авторизации
            id: Идентификатор вектора
            body: Полное тело запроса

        Returns:
            Ответ от API
        """
        return Req.patch(self.url_id(id), token, body)


class VectorGet(VectorRequestBody):
    """
    Класс для выполнения GET-запросов к API векторов.
    Наследует методы формирования URL от VectorRequestBody.
    """

    @staticmethod
    def get_vector(token: str) -> Any:
        """
        Отправляет GET-запрос для получения списка векторов.

        Args:
            token: Токен авторизации

        Returns:
            Ответ от API
        """
        return Req.get(env.VECTOR_URL, token)

    def get_id_vector(self, token: str, id: str) -> Any:
        """
        Отправляет GET-запрос для получения конкретного вектора по ID.

        Args:
            token: Токен авторизации
            id: Идентификатор вектора

        Returns:
            Ответ от API
        """
        return Req.get(self.url_id(id), token)

    def get_page_limit_q_vector(self, token: str, page: int, limit: int, q: str) -> Any:
        """
        Отправляет GET-запрос для получения списка векторов с пагинацией и поиском.

        Args:
            token: Токен авторизации для доступа к API
            page: Номер страницы для пагинации (начинается с 1)
            limit: Количество векторов на одной странице
            q: Поисковый запрос для фильтрации векторов

        Returns:
            Any: Ответ от API содержащий список векторов с метаданными пагинации

        Notes:
            - Поддерживает комбинированную пагинацию и поиск
            - Возвращает структуру с полями: vectors, paging, total_count
            - Поиск осуществляется по полям name и description векторов
        """
        return Req.get(self.url_page_limit_q(page, limit, q), token)


class VectorDelete(VectorRequestBody):
    """
    Класс для выполнения DELETE-запросов к API векторов.
    Наследует методы формирования URL от VectorRequestBody.
    """

    def delete_vector(self, token: str, id: str) -> Any:
        """
        Отправляет DELETE-запрос для удаления вектора по ID.

        Args:
            token: Токен авторизации
            id: Идентификатор вектора

        Returns:
            Ответ от API
        """
        return Req.delete(self.url_id(id), token)


class VectorResponse:
    """
    Класс для работы с ответами API векторов.
    """

    @staticmethod
    def get_response_vector(method: Any) -> Dict[str, Any]:
        """
        Получает полный ответ от API.

        Args:
            method: Результат выполнения запроса

        Returns:
            Полный ответ API в виде словаря
        """
        return Res.response_all(method)

    @staticmethod
    def get_response_vector_code(method: Any) -> int:
        """
        Получает статус-код из ответа API.

        Args:
            method: Результат выполнения запроса

        Returns:
            HTTP статус-код ответа
        """
        return Res.response_status_code(method)