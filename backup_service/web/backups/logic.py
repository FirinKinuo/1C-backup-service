import re

from pathlib import Path
from flask import send_file, Response, render_template

from backup_service.settings import config
from backup_service.filesystem import search
from backup_service.web.backups import models


def response_backup_files(base_name: str, backup_month: int) -> models.BackupResponse:
    """
    Получить ответ формата BackupResponse с данными путей до файлов
    Args:
        base_name (str): Название базы данных, для которой необходимо найти бэкапы
        backup_month (int): Месяц, в котором были созданны бекапы

    Returns:
        models.BackupResponse: Ответ формата BackupResponse
    """
    backup_files = search.search_backup_files(base_name=base_name, backup_month=backup_month)
    return models.BackupResponse(
        base_name=base_name,
        base_name_alias=base_name,
        month_id=backup_month,
        year_group=[models.BackupYearGroup(
            year=backup_year,
            files=[models.BackupFile(
                date=backup.backup_date(),
                file_url=str(backup.download_path()),
                size=backup.get_size()) for backup in backup_files if backup.backup_date().year == backup_year]
        ) for backup_year in [*{backup.backup_date().year for backup in backup_files}][::-1]]
    )


def response_download_backup(download_file: str) -> Response:
    """
    Получить ответ для скачивания файла бэкапа с сервера
    Args:
        download_file (str): Имя файла бекапа

    Returns:
        Response: Flask Response с файлом бэкапа или ошибку 404
    """
    download_path = Path(config.BACKUP_DIR, re.sub(r'(_\d{8}.+)', '', download_file), download_file)

    return send_file(path_or_file=f"{download_path}") if download_path.exists() else Response(status=404)


def response_backups_page() -> str:
    """
    Получить рендер страницы с бэкапами
    Returns:
        str: Строка срендренной страницы
    """
    return render_template(
        'backup_table.html',
        base_numbers=search.search_base_backup_folders()
    )
