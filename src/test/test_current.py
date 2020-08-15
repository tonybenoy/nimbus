import contextlib
from io import StringIO

import alembic
from sqlalchemy.orm import Session

from alembic.command import current as alembic_current

from nimbus.exceptions import *
from nimbus.models import (
    User,
    UserPy,
)


def test_current(getAlembic: alembic.config.Config) -> None:
    """Test that the alembic current command does not erorr"""
    stdout = StringIO()
    with contextlib.redirect_stdout(stdout):
        alembic_current(getAlembic, {})
    assert stdout.getvalue() == ""


def test_user2(session: Session) -> None:
    u = User(
        performed_by=123, user_id=101, name="dfd", fullname="dfdf", nickname="dfdd", email="asas",
    )
    session.add(u)
    session.commit()
    a = session.query(User).first()
    u = UserPy(
        id=a.id,
        performed_by=123,
        email="me@tonybeoy.com",
        user_id=101,
        name="dfd",
        fullname="dfdf",
        nickname="dfdd",
    )


def test_user(session: Session) -> None:
    u = User(
        performed_by=123, user_id=101, name="dfd", fullname="dfdf", nickname="dfdd", email="asas",
    )
    session.add(u)
    session.commit()
    a = session.query(User).first()
    u = UserPy(
        id=a.id,
        performed_by=123,
        email="me@tonybenoy.com",
        user_id=101,
        name="dfd",
        fullname="dfdf",
        nickname="dfdd",
    )
