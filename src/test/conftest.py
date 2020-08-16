# pylint: disable=redefined-outer-name,no-member

import contextlib
import os
import time
from pathlib import Path
from typing import (
    Dict,
    Iterator,
    Type,
)

import alembic
import psycopg2
import pytest
import sqlalchemy
from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from parse import (
    Result,
    parse,
)
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

import docker

REPO_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent.parent.resolve()

PYTEST_DB = "postgresql://test_user:test123@localhost:5680/test_db"


def build_alembic_config(engine: Engine) -> AlembicConfig:
    """Populate alembic configuration from metadata and config file."""
    print(REPO_ROOT)
    path_to_alembic_ini = REPO_ROOT / "alembic.ini"

    alembic_cfg = AlembicConfig(path_to_alembic_ini)
    alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))
    alembic_cfg.set_main_option(
        "script_location", str((Path("src") / "migrations" / "alembic_config"))
    )
    return alembic_cfg


@pytest.fixture(scope="session")
def docker_client() -> docker.DockerClient:
    return docker.from_env()


@pytest.fixture(scope="session")
def postgres_server(docker_client: docker.DockerClient) -> Iterator[Dict[str, str]]:
    connection_template = "postgresql://{user}:{pw}@{host}:{port:d}/{db}"
    conn_args = parse(connection_template, PYTEST_DB)
    container_name = "test_postgres"

    cont = None

    # Don't attempt to instantiate a container if
    # we're on CI
    if "GITHUB_SHA" not in os.environ:
        try:
            cont = docker_client.containers.get(container_name)
        except Exception as e:
            cont = docker_client.containers.run(
                image="postgres:12.4-alpine",
                name=container_name,
                detach=True,
                auto_remove=True,
                remove=True,
                ports={5432: conn_args["port"]},
                environment={
                    "POSTGRES_DB": f"{conn_args['db']}",
                    # 'POSTGRES_HOST_AUTH_METHOD': 'trust',
                    "POSTGRES_USER": f"{conn_args['user']}",
                    "POSTGRES_PASSWORD": f"{conn_args['pw']}",
                },
                healthcheck={
                    "test": ["CMD", "pg_isready"],
                    "interval": 1000000 * 10000,
                    "timeout": 1000000 * 3000,
                    "retries": 10,
                },
            )
    wait_for_postgres(conn_args)
    engine = create_engine(PYTEST_DB, echo=True)
    session_factory = sessionmaker(bind=engine)

    alembic_cfg = build_alembic_config(engine)
    _db = {
        "engine": engine,
        "session_factory": session_factory,
        "alembic_cfg": alembic_cfg,
    }

    yield _db

    if "GITHUB_SHA" not in os.environ:
        assert cont is not None
        cont.stop(timeout=1)


@pytest.fixture(scope="session")
def pg(postgres_server: Dict[str, str]) -> Iterator[Dict[str, str]]:
    upgrade_db(postgres_server, "head")
    yield postgres_server
    downgrade_db(postgres_server, "base")


def wait_for_postgres(conn_args: Result) -> None:
    while True:
        try:
            with contextlib.closing(
                psycopg2.connect(
                    host=conn_args["host"],
                    port=conn_args["port"],
                    user=conn_args["user"],
                    password=conn_args["pw"],
                    database=conn_args["db"],
                )
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("select 1;")
                    break
        except psycopg2.Error:
            time.sleep(0.1)


def upgrade_db(postgres_server: Dict[str, str], revision: str) -> None:
    alembic_upgrade(config=postgres_server["alembic_cfg"], revision=revision)


def downgrade_db(postgres_server: Dict[str, str], revision: str) -> None:
    alembic_downgrade(config=postgres_server["alembic_cfg"], revision=revision)


@pytest.fixture(scope="function")
def getAlembic(pg: Dict[str, AlembicConfig]) -> Iterator[AlembicConfig]:
    alembic_cfg = pg["alembic_cfg"]
    yield alembic_cfg


@pytest.fixture(scope="function")
def session(
    pg: Dict[str, Type[sqlalchemy.orm.session.Session]]
) -> Iterator[sqlalchemy.orm.session.Session]:
    session = pg["session_factory"]()
    yield session

    session.rollback()
    session.close()
