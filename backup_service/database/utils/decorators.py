import threading

from sqlalchemy.exc import SQLAlchemyError

from backup_service.database import session

INSERTION_LOCK = threading.RLock()


def with_insertion_lock(func):
    """Блокирует поток при выполнении добавления записи"""
    def insertion_lock(*args, **kwargs):
        with INSERTION_LOCK:
            return func(*args, **kwargs)

    return insertion_lock


def inserting_errors_handling(func):
    def error_handling(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as err:
            session.rollback()
            raise ValueError(*err.args) from err
        finally:
            session.close()

    return error_handling
