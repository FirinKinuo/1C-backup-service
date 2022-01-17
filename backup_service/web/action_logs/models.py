from datetime import datetime

from pydantic import BaseModel, conint


class ActionLogsPaginatorQuery(BaseModel):
    """Модель получения пагинации логов действий"""
    page: conint(gt=0)
    per_page: conint(gt=0)


class ActionLogsModel(BaseModel):
    """Модель логов действий пользователей"""
    id: int
    ip: str
    user: str
    type: str
    date: datetime
    message: str
