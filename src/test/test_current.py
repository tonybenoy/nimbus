import contextlib
from io import StringIO

import alembic
from alembic.command import current as alembic_current
from sqlalchemy.orm import Session

from nimbus.exceptions import *
from nimbus.models.models import User
from nimbus.models.pydantic_models import UserPy
from nimbus.utils import get_current_ist_time


def test_current(getAlembic: alembic.config.Config) -> None:
    """Test that the alembic current command does not erorr"""
    stdout = StringIO()
    with contextlib.redirect_stdout(stdout):
        alembic_current(getAlembic, {})
    assert stdout.getvalue() == ""


def test_user(session: Session) -> None:
    User.new(
        session=session,
        performed_by=1,
        user_id=1,
        first_name="tony",
        last_name="benoy",
        email="me@tonybenoy.com",
    )
    session.commit()
    a = session.query(User).first()
    UserPy(
        id=a.id,
        performed_by=a.performed_by,
        email=a.email,
        user_id=a.user_id,
        first_name=a.first_name,
        last_name=a.last_name,
        updated_at=a.updated_at,
        created_at=a.created_at,
        extra_details=a.extra_details,
    )
