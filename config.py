import os
from functools import lru_cache


class BaseConfig:
    MONGO_URI: str = os.getenv("MONGO_URI")
    REDIS_URL: str = os.getenv("REDIS_URL")
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND: str = os.environ.get(
        "CELERY_RESULT_BACKEND", REDIS_URL)
    JWT_SALT: str = os.getenv("JWT_SALT", '')
    FASTAPI_ENV: str = os.getenv("FASTAPI_ENV", "development")


class DevelopmentConfig(BaseConfig):
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    FASTAPI_ENV = "development"


class ProductionConfig(BaseConfig):
    FASTAPI_ENV = "production"
    pass


class TestingConfig(BaseConfig):
    MONGO_URI = os.getenv(
        "TEST_MONGO_URI", "mongodb://localhost:27017/")
    REDIS_URL = os.getenv("TEST_REDIS_URL", "redis://localhost:6379")
    FASTAPI_ENV = "testing"


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("FASTAPI_ENV", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
