from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Column,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from nimbus.utils import get_current_ist_time

Base = declarative_base()


class AuditMixin(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=get_current_ist_time(), nullable=True)
    updated_at = Column(TIMESTAMP, default=get_current_ist_time(), nullable=True)
    performed_by = Column(Integer, default=666, nullable=True)
    row_status = Column(String(50), nullable=False)

    @classmethod
    def snapshot(
        cls,
        primary_key: str,
        new_data: dict,
        session: Session,
        skip_columns: tuple = ("id", "created_at", "updated_at"),
    ):
        old_row = (
            session.query(cls)
            .filter(
                getattr(cls, primary_key) == new_data[primary_key],
                getattr(cls, "row_status") == "active",
            )
            .with_for_update(skip_locked=True)
            .one_or_none()
        )
        if old_row:
            old_row.row_status = "inactive"
            session.flush()
        cls_keys = cls.__table__.columns.keys()
        keys_to_skip = [key for key in new_data.keys() if key not in cls_keys]
        new_skip_columns = keys_to_skip + list(skip_columns)
        for column in new_skip_columns:
            new_data.pop(column, None)
        new_obj = cls.new(**new_data)
        session.flush()
        return new_obj

    @classmethod
    def new(cls, session: Session, **kwargs) -> Any:
        kwargs.update({"row_status": "active"})
        if "created_at" not in kwargs.keys():
            kwargs.update({"created_at": get_current_ist_time()})
        if "updated_at" not in kwargs.keys():
            kwargs.update({"updated_at": get_current_ist_time()})
        if "performed_by" not in kwargs.keys():
            kwargs.update({"performed_by": 666})
        obj = cls(**kwargs)
        session.add(obj)

        return obj

    def as_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return d

    def as_dict_for_json(self):
        d = {
            c.name: getattr(self, c.name).isoformat()
            if isinstance(getattr(self, c.name), datetime)
            else getattr(self, c.name)
            for c in self.__table__.columns
        }
        return d


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        params = dict((k, v) for k, v in kwargs.items())
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.flush()
        return instance


class User(AuditMixin):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    extra_details = Column(JSON, server_default="{}", nullable=True)
    email = Column(String(100))
    first_name = Column(String(50))
    last_name = Column(String(50))
