from typing import Optional

from backup_service.web import create_app
from backup_service.settings import config


def main(host: Optional[str] = None, port: Optional[int] = None, debug: Optional[bool] = None):
    """
    Запуск веб-сервера Flask. Не использовать в качестве сервера для продакшена!
    Лучше использовать связку с Nginx и Gunicorn
    Args:
        host (Optional[str]): Хост сервера
        port (Optional[int]): Порт сервера
        debug (Optional[bool]): Режим дебага

    Notes:
        Если не были переданы параметры в аргументах, то будут использованы параметры из файла конфигурации
    """
    flask_app = create_app()
    flask_app.run(
        host=host if host else config.WEB_HOST,
        port=port if port else config.WEB_PORT,
        debug=debug if debug else config.DEBUG
    )


if __name__ == '__main__':
    main()
