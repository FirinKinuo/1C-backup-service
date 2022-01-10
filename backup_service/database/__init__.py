from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from backup_service.settings.config import SQLITE_ENGINE


def create_session() -> scoped_session:
    """
    Создает сессию для подключения к базе данных
    Returns:
        scoped_session: Созданная сессия
    """
    engine = create_engine(SQLITE_ENGINE, connect_args={'check_same_thread': False})

    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=Base.metadata.bind, autoflush=False, expire_on_commit=False))


Base = declarative_base()
session = create_session()
