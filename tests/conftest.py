import importlib
import pytest


@pytest.fixture()
def tmp_db_path(tmp_path):
    return str((tmp_path / 'bot_test.db').absolute())


@pytest.fixture()
def db_module(tmp_db_path, monkeypatch):
    db = importlib.import_module('db')
    monkeypatch.setattr(db, 'DB_PATH', tmp_db_path, raising=False)
    db.init_db()

    return db


@pytest.fixture()
def main_module(db_module, monkeypatch):
    return importlib.import_module('main')


@pytest.fixture()
def openrouter_module():
    return importlib.import_module('openrouter_client')
