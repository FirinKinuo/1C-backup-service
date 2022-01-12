import re

from typing import Union
from pathlib import Path
from logging import getLogger

from flask import send_file, Response, render_template, g, redirect, request, session
from flask_simpleldap import LDAP

from backup_service.database import one_c_bases
from backup_service.settings import config
from backup_service.filesystem import search
from backup_service.web.backups import models

ldap_manager = LDAP()
log = getLogger("Backup controller")


def response_backup_files(base_name: str, backup_month: int) -> models.BackupResponse:
    """
    Получить ответ формата BackupResponse с данными путей до файлов
    Args:
        base_name (str): Название базы данных, для которой необходимо найти бэкапы
        backup_month (int): Месяц, в котором были созданы бэкапы

    Returns:
        models.BackupResponse: Ответ формата BackupResponse
    """
    backup_files = search.search_backup_files(base_name=base_name, backup_month=backup_month)

    return models.BackupResponse(
        base_name=base_name,
        base_name_alias=(one_c_bases.OneCBases.get_last(original_name=base_name) or
                         one_c_bases.OneCBases(alias_name=base_name)).alias_name,
        files=sorted([models.BackupFile(
            date=backup.backup_date(),
            file_url=str(backup.download_path()),
            size=backup.get_size()) for backup in backup_files], reverse=True)
    )


def response_download_backup(download_file: str) -> Response:
    """
    Получить ответ для скачивания файла бэкапа с сервера
    Args:
        download_file (str): Имя файла бэкапа

    Returns:
        Response: Flask Response с файлом бэкапа или ошибку 404
    """
    download_path = Path(config.BACKUP_DIR, re.sub(r'(_\d{8}.*)|(_backup_?_\d{4}_\d{2}_\d{2}.*)', '', download_file),
                         download_file)
    return send_file(path_or_file=f"{download_path}") if download_path.exists() else Response(status=404)


def response_backups_page() -> str:
    """
    Получить рендер страницы с бэкапами
    Returns:
        str: Строка срендренной страницы
    """
    base_list = [(
        base_name,
        (one_c_bases.OneCBases.get_last(original_name=base_name) or
         one_c_bases.OneCBases(alias_name=base_name)).alias_name) for base_name in search.search_base_backup_folders()]
    return render_template(
        'backup_table.html',
        base_list=base_list,
        title="База бэкапов"
    )


def find_user_ldap_groups():
    """Поиск LDAP групп, в которых состоит пользователь"""
    g.user = None
    if 'user_id' in session:
        g.user = session['user_id']
        g.ldap_groups = [group.decode('utf-8') for group in ldap_manager.get_user_groups(user=session['user_id'])]
        log.debug(f"Found groups {g.ldap_groups} for user {g.user}")


def response_login_page(error_credentials: bool = False) -> Union[str, Response]:
    """
    Получить рендер страницы входа или перенаправление на главную страницу,
    если вход в аккаунт уже был произведен

    Args:
        error_credentials (bool): Отправить состояние ошибки в шаблон
    """
    return render_template(
        'login.html',
        error_credentials=error_credentials) if not g.user else redirect('/')


def response_login_user() -> Response:
    """Авторизация пользователя по LDAP"""
    ldap_username = request.form['ldap-username']
    ldap_password = request.form['ldap-password']

    found_user = ldap_manager.bind_user(ldap_username, ldap_password)

    if found_user is not None:
        session['user_id'] = ldap_username
        return redirect(request.args.get('next') or '/')

    return response_login_page(error_credentials=True)


def response_logout_user() -> Response:
    """Завершение сессии для пользователя"""
    session.pop('user_id', None)
    return redirect('/')
