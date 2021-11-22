import pytest

from tests.unit.web import init_flask_test_client


def test_render_backup_page(flask_client):
    response = flask_client.get('/')

    assert response.status_code == 200
    assert b'backup-filters' in response.data
    assert b'backup-list' in response.data
