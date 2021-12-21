import sys
import logging

from pathlib import Path

import yaml

log = logging.getLogger('init')
YAML_CONFIG_PATH = Path('/etc', '1c-backup-service', 'config.yaml')
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
        raise SystemExit(f"Невозможно найти файл конфигурации! Путь: {YAML_CONFIG_PATH}") from SystemExit


_config = get_config_from_yaml()

DEBUG = bool(_config.get('debug')) or False
FLASK_SECRET_KEY = _config.get('flask_secret_key')
WEB_HOST = _config.get('web_host') or 'localhost'
WEB_PORT = int(_config.get('web_port')) or 5080

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

BACKUP_DIR = Path(_config.get('backup_dir')) if _config.get('backup_dir') else None
