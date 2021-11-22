from flask import Flask

from backup_service.settings import config
from backup_service.web import backups
from backup_service.web.backups import views


def create_app() -> Flask:
    """
    Создает приложение Flask

    Returns:
        Flask: Объект Flask с установленными настройками
    """
    app = Flask("1C BackupService", static_folder=None)
    app.debug = config.DEBUG
    app.testing = config.IS_TEST
    app.secret_key = config.FLASK_SECRET_KEY

    app.register_blueprint(blueprint=backups.blueprint, url_prefix='/')

    with app.app_context():
        return app
