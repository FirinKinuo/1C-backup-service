import sys
import logging

import yaml

from pathlib import Path

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
        raise SystemExit(f"Невозможно найти файл конфигурации! Путь: {YAML_CONFIG_PATH}")


_config = get_config_from_yaml()

DEBUG = bool(_config.get('debug'))
FLASK_SECRET_KEY = _config.get('flask_secret_key')
WEB_HOST = _config.get('web_host')
WEB_PORT = int(_config.get('web_port'))

LDAP_TYPE = _config.get('ldap_type')
LDAP_HOST = _config.get('ldap_host')
LDAP_BASE_DN = _config.get('ldap_base_dn')
LDAP_USER_DN = _config.get('ldap_user_dn')
LDAP_GROUP_DN = _config.get('ldap_user_rdn_attr')
LDAP_USER_RDN_ATTR = _config.get('ldap_user_rdn_attr')
LDAP_USER_LOGIN_ATTR = _config.get('ldap_user_login_attr')
LDAP_BIND_USER_DN = _config.get('ldap_bind_user_dn')
LDAP_BIND_USER_PASSWORD = _config.get('ldap_bind_user_password')

BACKUP_DIR = Path(_config.get('backup_dir')) if _config.get('backup_dir') else None
