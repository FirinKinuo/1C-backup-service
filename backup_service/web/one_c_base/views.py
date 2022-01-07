from flask_simpleldap import LDAP
from flask_pydantic import validate

from backup_service.settings import config
from backup_service.web.one_c_base import blueprint, models, controllers

ldap_manager = LDAP()


@ldap_manager.group_required(groups=[config.LDAP_GROUP_ACCESS_MANAGE_BACKUPS])
@blueprint.put('/set-alias')
@validate(body=models.AliasNameQuery)
def view_set_alias() -> controllers.Response:
    return controllers.set_alias_base_name()
