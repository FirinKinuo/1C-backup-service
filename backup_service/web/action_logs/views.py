from flask_simpleldap import LDAP
from flask_pydantic import validate

from backup_service.settings import config
from backup_service.web.action_logs import blueprint, models, controllers

ldap_manager = LDAP()


@blueprint.get('/')
@ldap_manager.group_required(groups=[config.LDAP_GROUP_ACCESS_MANAGE_BACKUPS])
def view_action_logs() -> str:
    return controllers.response_action_logs_page()


@blueprint.get('/getActions')
@validate(query=models.ActionLogsPaginatorQuery)
@ldap_manager.group_required(groups=[config.LDAP_GROUP_ACCESS_MANAGE_BACKUPS])
def get_action_logs() -> controllers.Response:
    return controllers.response_action_logs_pagination()
