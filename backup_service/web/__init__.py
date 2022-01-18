from typing import Optional
from pathlib import Path
from datetime import timedelta

from flask import Flask
from flask_simpleldap import LDAP

from backup_service.settings import config
from backup_service.web import backups, one_c_base, action_logs
from backup_service.web.backups import views as backups_views
from backup_service.web.one_c_base import views as one_c_base_views
from backup_service.web.action_logs import views as action_logs_views

ldap_manager = LDAP()


def create_app(debug: Optional[bool] = None, test: Optional[bool] = None) -> Flask:
    """
    Создает приложение Flask

    Args:
        debug (Optional[bool]): Режим дебага
        test (Optional[bool]): Режим теста

    Returns:
        Flask: Объект Flask с установленными настройками
    """
    app = Flask("1C BackupService", template_folder=str(Path(__path__[0], 'templates')),
                static_folder=str(Path(__path__[0], 'static')))
    app.debug = debug if debug else config.DEBUG
    app.testing = test if test else config.IS_TEST
    app.secret_key = config.FLASK_SECRET_KEY

    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=config.FLASK_SESSION_LIFETIME)

    app.config['LDAP_HOST'] = config.LDAP_HOST
    app.config['LDAP_BASE_DN'] = config.LDAP_BASE_DN
    app.config['LDAP_USERNAME'] = config.LDAP_USERNAME
    app.config['LDAP_PASSWORD'] = config.LDAP_PASSWORD

    app.config['LDAP_GROUP_OBJECT_FILTER'] = config.LDAP_GROUP_OBJECT_FILTER
    app.config['LDAP_GROUPS_OBJECT_FILTER'] = config.LDAP_GROUPS_OBJECT_FILTER
    app.config['LDAP_GROUP_MEMBER_FILTER'] = config.LDAP_GROUP_MEMBER_FILTER
    app.config['LDAP_GROUP_MEMBER_FILTER_FIELD'] = config.LDAP_GROUP_MEMBER_FILTER_FIELD
    app.config['LDAP_USER_OBJECT_FILTER'] = config.LDAP_USER_OBJECT_FILTER
    app.config['LDAP_LOGIN_VIEW'] = 'backups.login_user'
    app.config['LDAP_OPENLDAP'] = config.LDAP_OPENLDAP

    app.register_blueprint(blueprint=backups.blueprint, url_prefix='/')
    app.register_blueprint(blueprint=one_c_base.blueprint, url_prefix='/one-c-base')
    app.register_blueprint(blueprint=action_logs.blueprint, url_prefix="/logs")
    ldap_manager.init_app(app=app)

    with app.app_context():
        return app
