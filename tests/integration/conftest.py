
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.connection import Base, get_db
from app.database.models import User, Calculation
from main import app


# Connect to the separate test database.
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_test_db"
)

test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True
)

Base.metadata.create_all(bind=test_engine)


@pytest.fixture
def client():
    """Provide an API test client with an isolated database transaction."""

    connection = test_engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False,
        join_transaction_mode="create_savepoint"
    )

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)

        transaction.rollback()
        connection.close()
