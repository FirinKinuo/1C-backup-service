import pytest

from backup_service.web import create_app


@pytest.fixture(scope="session", name='flask_client')
def init_flask_test_client():
    flask_app = create_app(debug=True, test=True)

    with flask_app.test_client() as test_client:
        yield test_client
