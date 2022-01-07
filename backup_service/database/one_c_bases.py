from sqlalchemy.sql import sqltypes, schema

from backup_service.database.base import BaseModel


class OneCBases(BaseModel):
    """Модель таблицы с данными баз 1С"""
    __tablename__ = 'one_c_bases'
    id = schema.Column(sqltypes.Integer, primary_key=True, autoincrement=True, unique=True)
    original_name = schema.Column(sqltypes.String(256), nullable=False, unique=True)
    alias_name = schema.Column(sqltypes.String(256), nullable=False)
    share = schema.Column(sqltypes.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<{self.id} | {self.alias_name} aka {self.original_name} || Shared: {self.share}>"

    def __eq__(self, other):
        return isinstance(other, OneCBases) and self.id == other.id


def init_tables():
    """Инициализация таблиц в базе данных"""
    OneCBases.__table__.create(checkfirst=True)


if __name__ != '__main__':
    init_tables()
