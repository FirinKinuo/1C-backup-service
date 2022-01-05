import pytest
import asyncio

from backup_service.database import one_c_bases, Base

__all__ = [
    'async_loop',
    'preload_database'
]


@pytest.fixture(scope='session')
def async_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
def preload_database():
    """Предзагрузка базы данных, очистка, инициализация таблиц"""
    Base.metadata.drop_all()
    one_c_bases.init_tables()
    yield
