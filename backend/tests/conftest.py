import sys
from pathlib import Path
import pytest

# เพิ่ม path ของ backend เข้าไปใน sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import app as flask_app
from models import db

@pytest.fixture
def app():
    flask_app.config.update(
        {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': f'sqlite:///:memory:',
        }
    )
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield
