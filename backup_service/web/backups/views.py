from flask_pydantic import validate

from backup_service.web.backups import blueprint, models, logic


@blueprint.get('/')
def view_backups() -> str:
    return logic.response_backups_page()


@blueprint.get('/getBackupFiles')
@validate(query=models.BackupQuery)
def view_backup_files(query: models.BackupQuery) -> models.BackupResponse:
    return logic.response_backup_files(base_name=query.base_name, backup_month=query.month_id)


@blueprint.get('/download')
@validate(query=models.BackupDownloadQuery)
def download_backup(query: models.BackupDownloadQuery) -> logic.Response:
    return logic.response_download_backup(download_file=query.backup)
