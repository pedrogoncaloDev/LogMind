import tempfile
import uuid
from pathlib import Path

import pytest
from sqlalchemy import create_engine

# `app.database.session` runs `Base.metadata.create_all(bind=engine)` as a
# module-level side effect against the real Postgres engine the moment it is
# imported. Every domain repository imports it, so before anything under
# `app` gets imported we swap `app.database.connection.engine` for a
# throwaway SQLite engine. That way the very first import of
# `app.database.session` (triggered below) creates the schema in SQLite
# instead of trying to reach a real Postgres server.
import app.database.connection as connection

_TEST_DB_PATH = Path(tempfile.gettempdir()) / f"logmind_test_{uuid.uuid4().hex}.db"
test_engine = create_engine(
    f"sqlite:///{_TEST_DB_PATH}",
    connect_args={"check_same_thread": False},
)
connection.engine = test_engine

import app.database.session  # noqa: E402  (import order is load-bearing, see above)
from app.database.base import Base  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.domains.users.model import User  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_database():
    """Give every test a clean schema so rows from one test never leak into another."""
    yield
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


@pytest.fixture
def db_session():
    from app.database.session import SessionLocal

    with SessionLocal() as session:
        yield session


@pytest.fixture
def app_instance():
    from app.main import app

    return app


@pytest.fixture
def client(app_instance):
    from starlette.testclient import TestClient

    with TestClient(app_instance) as test_client:
        yield test_client


@pytest.fixture
def storage_dir(tmp_path, monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "STORAGE_LOCAL_PATH", str(tmp_path))
    return tmp_path


@pytest.fixture
def existing_user(db_session):
    plain_password = "senha12345"
    user = User(
        name="Existing User",
        email="existing.user@example.com",
        password_hash=hash_password(plain_password),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user, plain_password


@pytest.fixture
def inactive_user(db_session):
    plain_password = "senha12345"
    user = User(
        name="Inactive User",
        email="inactive.user@example.com",
        password_hash=hash_password(plain_password),
        is_active=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user, plain_password


@pytest.fixture
def auth_headers(existing_user):
    from app.core.security import create_access_token

    user, _ = existing_user
    token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return {"Authorization": f"Bearer {token}"}
