from functools import total_ordering
from typing import Optional
from datetime import date

from pydantic import BaseModel


@total_ordering
class BackupFile(BaseModel):
    """Модель данных бэкап файла"""
    date: date
    file_url: str
    size: int

    def __eq__(self, other):
        return self.date == other.date

    def __lt__(self, other):
        return self.date < other.date


class BackupQuery(BaseModel):
    """Модель запроса бэкап файла"""
    base_name: str
    month_id: int


class BackupResponse(BaseModel):
    """Модель ответа на запрос данных файла бэкапа"""
    base_name: str
    base_name_alias: Optional[str]
    files: list[BackupFile]


class BackupDownloadQuery(BaseModel):
    """Модель запроса на скачивание файла бэкапа"""
    backup: str
