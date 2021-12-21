from typing import Union

from flask_simpleldap import LDAP
from flask_pydantic import validate

from backup_service.web.backups import blueprint, models, controllers


ldap_manager = LDAP()


@blueprint.before_app_request
def before_request():
    controllers.find_user_ldap_groups()


@blueprint.get('/login')
def view_login_page() -> str:
    return controllers.response_login_page()


@blueprint.post('/login')
def login_user() -> Union[str, controllers.Response]:
    return controllers.response_login_user()


@blueprint.get('/')
@ldap_manager.group_required(groups=['Access_backups'])
def view_backups() -> str:
    return controllers.response_backups_page()


@blueprint.get('/getBackupFiles')
@validate(query=models.BackupQuery)
@ldap_manager.group_required(groups=['Access_backups'])
def view_backup_files(query: models.BackupQuery) -> models.BackupResponse:
    return controllers.response_backup_files(base_name=query.base_name, backup_month=query.month_id)


@blueprint.get('/download')
@validate(query=models.BackupDownloadQuery)
@ldap_manager.group_required(groups=['Access_backups'])
def download_backup(query: models.BackupDownloadQuery) -> controllers.Response:
    return controllers.response_download_backup(download_file=query.backup)


@blueprint.get('/logout')
def logout_user() -> controllers.Response:
    return controllers.response_logout_user()
