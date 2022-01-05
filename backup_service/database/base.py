from typing import Union

from backup_service.database import Base, session
from backup_service.database.utils import filters, decorators


class BaseModel(Base):
    """Базовая модель"""
    __abstract__ = True

    @classmethod
    @decorators.with_insertion_lock
    @decorators.inserting_errors_handling
    def set_or_get(cls, **kwargs) -> 'BaseModel':
        """Создать или получить существующую модель"""
        required_fields = cls.__table__.columns.keys()
        filtered_kwargs = filters.leave_required_keys(kwargs, required_fields)
        required_fields.remove('id')

        # Проверка того, что все необходимые поля были переданы
        if set(required_fields) - set(filtered_kwargs):
            raise KeyError(f"""Не были переданы необходимые поля: {set(required_fields) - set(filtered_kwargs)}""")

        record = session.query(cls).filter_by(**filtered_kwargs).limit(1).scalar()
        if not record:
            if 'id' in filtered_kwargs:
                filtered_kwargs.pop('id')

            record = cls(**filtered_kwargs)
            session.add(record)
            session.commit()

        return record

    @classmethod
    def get_all(cls, **kwargs) -> list['BaseModel']:
        """Получить все записи"""
        required_fields = cls.__table__.columns.keys()
        filtered_kwargs = filters.leave_required_keys(kwargs, required_fields)

        return session.query(cls).filter_by(**filtered_kwargs).all()

    @classmethod
    def get_last(cls, **kwargs) -> Union['BaseModel', None]:
        """Получить последнюю запись по переданным данным"""
        required_fields = cls.__table__.columns.keys()
        filtered_kwargs = filters.leave_required_keys(kwargs, required_fields)

        return session.query(cls).filter_by(**filtered_kwargs).limit(1).scalar()

    @decorators.with_insertion_lock
    @decorators.inserting_errors_handling
    def update(self, update: dict) -> 'BaseModel':
        """
        Обновить данные полей записи
        Args:
            update (dict): Словарь полей с обновленными значениями

        Returns:
            BaseModel - Экземпляр класса с обновленными данными
        """
        session.query(self.__class__).filter_by(id=self.id).update(update)
        session.commit()

        self.__dict__ |= update  # Слияние словарей для обновления записей класса
        return self
