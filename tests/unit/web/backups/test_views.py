import pytest
from datetime import date
from backup_service.web.backups import models, views

from tests.unit.web import init_flask_test_client


@pytest.fixture()
def mock_response_backups_page(mocker):
    def mock(response_page: str):
        mocker.patch.object(views.logic, 'response_backups_page',
                            return_value=response_page)

    return mock


@pytest.fixture()
def mock_response_backup_files(mocker):
    def mock(response_data: models.BackupResponse):
        mocker.patch.object(views.logic, 'response_backup_files',
                            return_value=response_data)

    return mock


@pytest.fixture()
def mock_response_download_backup(mocker):
    def mock(response_data: views.logic.Response):
        mocker.patch.object(views.logic, 'response_download_backup',
                            return_value=response_data)

    return mock


def test_render_backup_page(flask_client, mock_response_backups_page):
    page_payload = "test_page"
    mock_response_backups_page(response_page=page_payload)

    response = flask_client.get('/')

    assert response.status_code == 200
    assert page_payload.encode() == response.data


def test_get_backup_files(flask_client, mock_response_backup_files):
    request_payload = models.BackupQuery(base_name="111_test_base", month_id=12)
    response_data = models.BackupResponse(
        base_name=request_payload.base_name,
        base_name_alias=request_payload.base_name,
        month_id=request_payload.month_id,
        files=[models.BackupFile(
            date=date(year=2021, month=request_payload.month_id, day=10),
            file_url=request_payload.base_name,
            size=0)])
    mock_response_backup_files(response_data=response_data)

    response = flask_client.get('/getBackupFiles', query_string=request_payload)

    assert response.status_code == 200
    assert models.BackupResponse(**response.json) == response_data


def test_missing_query_get_backup_files(flask_client):
    response = flask_client.get('/getBackupFiles')

    assert response.status_code == 400

    for missing_query in response.json['validation_error']['query_params']:
        assert missing_query['loc'][0] in ['base_name', 'month_id']


def test_download_backup_files(flask_client, mock_response_download_backup):
    request_payload = models.BackupDownloadQuery(backup="111_test_base.bak")
    response_data = views.logic.Response(status=200)
    mock_response_download_backup(response_data=response_data)

    response = flask_client.get('/download', query_string=request_payload)

    assert response.status_code == 200


def test_missing_query_download_backup_files(flask_client, mock_response_download_backup):
    response = flask_client.get('/download')

    assert response.status_code == 400

    for missing_query in response.json['validation_error']['query_params']:
        assert missing_query['loc'][0] in ['backup']