import os
import pytest
import time
from pathlib import Path
import requests
from requests.exceptions import ConnectionError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.exc import OperationalError

from app.infrastructure.persistence_sqla.mappings.orm import map_tables
from app.infrastructure.persistence_sqla.registry import mapper_registry

from app.setup.config.loader import ValidEnvs
from app.setup.config.settings import load_settings

settings = load_settings(ValidEnvs.DEV)
postgres_uri = settings.postgres.dsn

host = os.environ.get("API_HOST", "localhost")
port = 8000 if host == "localhost" else 80
fast_api_url = f"http://{host}:{port}"

# @pytest.fixture
# def postgres_uri() -> str:
#     settings = load_settings(ValidEnvs.DEV)
#     return settings.postgres.dsn

@pytest.fixture
def api_url() -> str:
    return fast_api_url


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    map_tables()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
    

def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Postgres never came up")


def wait_for_webapp_to_come_up():
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return requests.get(fast_api_url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail("API never came up")


@pytest.fixture(scope="session")
def postgres_db():
    engine = create_engine(postgres_uri)
    wait_for_postgres_to_come_up(engine)
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db):
    map_tables()
    yield sessionmaker(bind=postgres_db)()
    clear_mappers()


@pytest.fixture
def restart_api():
    (Path(__file__).parent / "../src/app/run.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()