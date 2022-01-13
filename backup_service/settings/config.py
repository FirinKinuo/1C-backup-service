import sys
import logging

from pathlib import Path

import yaml

log = logging.getLogger('init')
EXTERNAL_FILES_DIR = Path('/etc', '1c-backup-service')
YAML_CONFIG_PATH = Path(EXTERNAL_FILES_DIR, 'config.yaml')
IS_TEST = any(map(lambda path: 'tests' in path, sys.path))  # Если найдены пути тестов, то переходим в режим теста


def get_config_from_yaml() -> dict:
    """
    Получение конфигурации из файла .yaml

    Returns:
        (dict): Словарь с конфигурацией из .yaml файла
    """
    try:
        with open(YAML_CONFIG_PATH, 'r', encoding="utf-8") as config_file:
            return yaml.load(stream=config_file, Loader=yaml.loader.SafeLoader)
    except FileNotFoundError:
        error_message = f"Невозможно найти файл конфигурации! Путь: {YAML_CONFIG_PATH}"
        raise SystemExit(error_message) from SystemExit


_config = get_config_from_yaml()

DEBUG = bool(_config.get('debug')) or False
LOGGER_LEVEL = logging.getLevelName(_config.get('log_level').upper())
FLASK_SECRET_KEY = _config.get('flask_secret_key')

LDAP_TYPE = _config.get('ldap_type')
LDAP_HOST = _config.get('ldap_host')
LDAP_BASE_DN = _config.get('ldap_base_dn')
LDAP_USERNAME = _config.get('ldap_username')
LDAP_PASSWORD = _config.get('ldap_password')

LDAP_GROUP_OBJECT_FILTER = _config.get('ldap_group_object_filter')
LDAP_GROUPS_OBJECT_FILTER = _config.get('ldap_groups_object_filter')
LDAP_GROUP_MEMBER_FILTER = _config.get('ldap_group_member_filter')
LDAP_GROUP_MEMBER_FILTER_FIELD = _config.get('ldap_group_member_filter_field')
LDAP_USER_OBJECT_FILTER = _config.get('ldap_user_object_filter')

LDAP_GROUP_ACCESS_BACKUP_TABLE = _config.get('ldap_group_access_backup_table') or ''
LDAP_GROUP_ACCESS_BACKUP_DOWNLOAD = _config.get('ldap_group_access_backup_download') or ''
LDAP_GROUP_ACCESS_MANAGE_BACKUPS = _config.get('ldap_group_access_manage_backups') or ''
LDAP_OPENLDAP = _config.get('ldap_openldap') or False

BACKUP_DIR = Path(_config.get('backup_dir')) if _config.get('backup_dir') else None

SQLITE_ENGINE = f"sqlite:///{Path(EXTERNAL_FILES_DIR, _config.get('sqlite_path'))}"

logging.basicConfig(level=LOGGER_LEVEL,
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                    datefmt="%d/%b/%Y %H:%M:%S",
                    filename="/var/log/1c-backup-service/backups.log" if not DEBUG else None,
                    filemode='a')

werkzeug_log = logging.getLogger('werkzeug')
werkzeug_log.setLevel(logging.ERROR if not DEBUG else logging.DEBUG)
