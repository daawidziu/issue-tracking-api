import pytest

from application import init_app


@pytest.fixture
def app():
    app = init_app("config.TestingConfig")
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
