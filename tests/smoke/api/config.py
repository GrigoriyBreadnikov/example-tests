import os
from dataclasses import dataclass
from dotenv import load_dotenv


class EnvLoader:
    """Универсальный загрузчик переменных окружения"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        """Загрузка переменных с приоритетами:
        1. Существующие переменные окружения
        2. Файл .env (только локально)
        3. Явная ошибка если чего-то не хватает
        """
        required_vars = {"USER", "VECTOR_URL", "TOKEN_URL", "PASSWORD", "CLIENT_ID", "GRANT_TYPE", "SCOPE"}

        load_dotenv(override=True)

        # Проверяем все переменные
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise RuntimeError(
                f"Не хватает переменных окружения: {', '.join(missing)}\n"
                "Для локальной разработки создайте .env файл\n"
                "В GitLab CI добавьте Variables в настройках CI/CD"
            )


@dataclass
class VarEnv:
    """Конфигурация приложения"""

    USERNAME: str
    VECTOR_URL: str
    TOKEN_URL: str
    PASSWORD: str
    CLIENT_ID: str
    GRANT_TYPE: str
    SCOPE: str
    SECRET: str

    @classmethod
    def load(cls):
        """Основной метод инициализации"""
        EnvLoader()  # Загружаем переменные

        return cls(
            USERNAME=os.environ["USER"],
            VECTOR_URL=os.environ["VECTOR_URL"],
            TOKEN_URL=os.environ["TOKEN_URL"],
            PASSWORD=os.environ["PASSWORD"],
            CLIENT_ID=os.environ["CLIENT_ID"],
            GRANT_TYPE=os.environ["GRANT_TYPE"],
            SCOPE=os.environ["SCOPE"],
            SECRET=os.environ["SECRET"],
        )


# Глобальный экземпляр для загрузки энвов при многопоточности (pytest -n auto)
env = VarEnv.load()
