import yaml
import logging
import sys

from pathlib import Path
from yaml import loader

log = logging.getLogger('init')
YAML_CONFIG_PATH = Path('/etc', '1c_', 'config.yaml')
IS_TEST = any(map(lambda path: 'tests' in path, sys.path))  # Если найдены пути тестов, то переходим в режим теста


def get_config_from_yaml() -> dict:
    """
    Получение конфигурации из файла .yaml

    Returns:
        (dict): Словарь с конфигурацией из .yaml файла
    """
    try:
        with open(YAML_CONFIG_PATH, 'r', encoding="utf-8") as config_file:
            return yaml.load(stream=config_file, Loader=loader.SafeLoader)
    except FileNotFoundError:
        log.critical(f"Невозможно найти файл конфигурации! Путь: {YAML_CONFIG_PATH}")
        exit(1)


_config = get_config_from_yaml()


