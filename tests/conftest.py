import os

os.environ["JWT_SECRET"] = "test-only-secret-not-for-deployment-123456789"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
from application import create_app
from database import get_db


@pytest.fixture
def client(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'piazza-test.db'}",
        connect_args={"check_same_thread": False},
    )
    sessions = sessionmaker(bind=engine)
    app = create_app(engine)

    with sessions() as session:
        session.add_all([
            models.Topic(name="Politics"),
            models.Topic(name="Health"), 
            models.Topic(name="Sport"),
            models.Topic(name="Tech")
        ])
        session.commit()

    def override_db():
        with sessions() as session:
            yield session

    app.dependency_overrides[get_db] = override_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()