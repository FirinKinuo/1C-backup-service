from typing import Optional

from flask import Flask

from backup_service.settings import config
from backup_service.web import backups
from backup_service.web.backups import views


def create_app(debug: Optional[bool] = None, test: Optional[bool] = None) -> Flask:
    """
    Создает приложение Flask

    Args:
        debug (Optional[bool]): Режим дебага
        test (Optional[bool]): Режим теста

    Returns:
        Flask: Объект Flask с установленными настройками
    """
    app = Flask("1C BackupService", static_folder=None)
    app.debug = debug if debug else config.DEBUG
    app.testing = test if test else config.IS_TEST
    app.secret_key = config.FLASK_SECRET_KEY

    app.register_blueprint(blueprint=backups.blueprint, url_prefix='/')

    with app.app_context():
        return app
