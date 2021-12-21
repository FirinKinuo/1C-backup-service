import re

from pathlib import Path
from backup_service.settings import config
from backup_service.filesystem import path


def search_backup_files(base_name: str, backup_month: int) -> list[path.BackupPath]:
    """
    Поиск файлов бэкапов переданной базы
    Args:
        base_name (str): Название базы данных, для которой необходимо получить файлы бэкапов
        backup_month (int): Месяц, в котором был создан бэкап

    Returns:
        list[path.BackupPath]: Список BackupPath до файлов бэкапов
    """
    base_backup_folder = Path(config.BACKUP_DIR, base_name)

    if not base_backup_folder.exists():
        raise FileNotFoundError(f"Бекапы для базы {base_name} по пути {base_backup_folder} не найдены!")

    return list(file for file in map(path.BackupPath, base_backup_folder.rglob(f'*{backup_month}*.bak'))
                if file.backup_date().month == backup_month)


def search_base_backup_folders() -> list[str]:
    """
    Поиск папок бэкапов баз
    Returns:
        list[str]: Список названий папок с бэкапами
    """
    return [backup_path.name for backup_path in config.BACKUP_DIR.iterdir()
            if re.search(r'(^\d+.+)', backup_path.name)]
