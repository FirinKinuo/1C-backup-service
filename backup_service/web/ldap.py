from flask import current_app as flask_app
from flask_ldap3_login import LDAP3LoginManager

from backup_service.settings import config


def _configure_ldap() -> LDAP3LoginManager:
    """
    Сконфигурировать LDAP
    Returns:
        LDAP3LoginManager: Сконфигурированный объект LDAP3LoginManager
    """
    flask_app.config['LDAP_HOST'] = config.LDAP_HOST
    flask_app.config['LDAP_BASE_DN'] = config.LDAP_BASE_DN
    flask_app.config['LDAP_USER_DN'] = config.LDAP_USER_DN
    flask_app.config['LDAP_GROUP_DN'] = config.LDAP_GROUP_DN
    flask_app.config['LDAP_USER_RDN_ATTR'] = config.LDAP_USER_RDN_ATTR
    flask_app.config['LDAP_USER_LOGIN_ATTR'] = config.LDAP_USER_LOGIN_ATTR
    flask_app.config['LDAP_BIND_USER_DN'] = config.LDAP_BIND_USER_DN
    flask_app.config['LDAP_BIND_USER_PASSWORD'] = config.LDAP_BIND_USER_PASSWORD

    return LDAP3LoginManager(app=flask_app)


ldap_manager = _configure_ldap()
