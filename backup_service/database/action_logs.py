from sqlalchemy.sql import sqltypes, schema

from backup_service.database import base

TYPE_LOGIN = "login"
TYPE_DOWNLOAD = "download"
TYPE_CHANGE = "change"


class ActionLogs(base.BaseModel):
    """Модель таблицы логов действий сервиса"""
    __tablename__ = 'action_logs'
    ip = schema.Column(sqltypes.CHAR(14), nullable=True)
    user = schema.Column(sqltypes.CHAR(128), nullable=False)
    type = schema.Column(sqltypes.CHAR(24), nullable=False)
    date = schema.Column(sqltypes.DateTime(timezone=True), nullable=False)
    message = schema.Column(sqltypes.VARCHAR(), nullable=False)

    def __repr__(self):
        return f"{self.id} | Type: {self.type} at {self.date}"


def init_tables():
    """Инициализация таблиц в базе данных"""
    ActionLogs.__table__.create(checkfirst=True)


if __name__ != "__main__":
    init_tables()
