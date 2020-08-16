from sqlalchemy import (
    JSON,
    Column,
    Integer,
    String,
)

from nimbus.models.base import AuditMixin


class User(AuditMixin):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    extra_details = Column(JSON, server_default="{}", nullable=True)
    email = Column(String(100))
    first_name = Column(String(50))
    last_name = Column(String(50))


class UserMaster(AuditMixin):
    __tablename__ = "user_master"
    user_id = Column(Integer, primary_key=True)
    mobile = Column(String(13))


class Products(AuditMixin):
    __tablename__ = "products"
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(13))
    item_description = Column(JSON, server_default="{}", nullable=True)
    measure = Column(String(13))


class Merchant(AuditMixin):
    __tablename__ = "merchant"
    merchant_id = Column(Integer, primary_key=True)
    email = Column(String(50))
    extra_details = Column(JSON, server_default="{}", nullable=True)
