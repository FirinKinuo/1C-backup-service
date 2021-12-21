from typing import Optional
from datetime import date

from pydantic import BaseModel


class BackupFile(BaseModel):
    """Модель данных бэкап файла"""
    date: date
    file_url: str
    size: int


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
