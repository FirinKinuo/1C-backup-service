from flask_simpleldap import LDAP
from flask_pydantic import validate

from backup_service.settings import config
from backup_service.web.one_c_base import blueprint, models, controllers

ldap_manager = LDAP()


@blueprint.put('/set-alias')
@ldap_manager.group_required(groups=[config.LDAP_GROUP_ACCESS_MANAGE_BACKUPS])
@validate(body=models.OneCBaseModel)
def view_set_alias() -> tuple[models.OneCBaseNames, int]:
    return controllers.set_alias_base_name()


@blueprint.get('/names')
@ldap_manager.group_required(groups=[config.LDAP_GROUP_ACCESS_MANAGE_BACKUPS])
def view_get_one_c_bases_name_list() -> controllers.Response:
    return controllers.response_get_one_c_bases_name_list()


@blueprint.get('/aliases')
@ldap_manager.group_required(groups=[config.LDAP_GROUP_ACCESS_MANAGE_BACKUPS])
def view_aliases() -> str:
    return controllers.response_aliases_page()

