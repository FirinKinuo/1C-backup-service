from typing import Union
from functools import total_ordering

from sqlalchemy.sql import sqltypes, schema

from backup_service.database import Base, session
from backup_service.database.utils import filters, decorators


@total_ordering
class BaseModel(Base):
    """Базовая модель"""
    __abstract__ = True
    id = schema.Column(sqltypes.Integer, primary_key=True, autoincrement=True, unique=True)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    @classmethod
    def _filter_input(cls, **kwargs: dict) -> dict:
        """Очищает ввод от ненужных аргументов"""
        required_fields = cls.__table__.columns.keys()
        filtered_kwargs = filters.leave_required_keys(kwargs, required_fields)
        required_fields.remove('id')

        # Проверка того, что все необходимые поля были переданы
        if set(required_fields) - set(filtered_kwargs):
            raise KeyError(f"""Не были переданы необходимые поля: {set(required_fields) - set(filtered_kwargs)}""")

        return filtered_kwargs

    @classmethod
    @decorators.with_insertion_lock
    @decorators.inserting_errors_handling
    def set_or_get(cls, **kwargs) -> 'BaseModel':
        """Создать или получить существующую модель"""
        filtered_kwargs = cls._filter_input(**kwargs)
        record = session.query(cls).filter_by(**filtered_kwargs).limit(1).scalar()
        if not record:
            if 'id' in filtered_kwargs:
                filtered_kwargs.pop('id')

            record = cls(**filtered_kwargs)
            session.add(record)
            session.commit()

        return record

    @classmethod
    @decorators.with_insertion_lock
    @decorators.inserting_errors_handling
    def set(cls, **kwargs) -> 'BaseModel':
        """Создать новую запись в таблицу"""
        filtered_kwargs = cls._filter_input(**kwargs)

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

    @classmethod
    def get_pool_with_offset(cls, offset: int, pool: int) -> list['BaseModel']:
        """
        Получить список записей с смещением
        Args:
            offset (int): Смещение в списке
            pool (int): Количество записей

        Returns:
            list[BaseModel] - Список записей данной модели
        """
        return session.query(cls).order_by(cls.id.desc()).offset(offset).limit(pool).all()
