import re
import os

from datetime import date, datetime

from pathlib import PosixPath, WindowsPath, Path


class BackupPath(PosixPath if os.name == 'posix' else WindowsPath):
    """Модификация Path от pathlib для работы с путями до бэкап файлов"""

    def download_path(self) -> Path:
        """
        Путь для безопасного распространения в сети
        Returns:
            str: Относительный путь до папки и файла с бэкапом backup_dir/backup_file.bak
        """

        return Path(self.name)

    def backup_date(self) -> date:
        """
        Получить дату создания бэкапа
        Returns:
            data: Дата создания бэкапа
        """
        matched_date = re.search(r'(\d{8})', self.stem)
        if matched_date is None:
            matched_date = re.search(r'\d{4}_\d{2}_\d{2}', self.stem)

        return datetime.strptime(matched_date.group().replace('_', ''), '%Y%m%d').date()

    def get_size(self) -> float:
        """
        Получить размер файла бекапа в МегаБайтах
        Returns:
            float: Размер файла
        """
        return os.path.getsize(self) / 1024 / 1024
