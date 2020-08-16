from decimal import Decimal
from typing import Dict

from pydantic import EmailStr
from pydantic.dataclasses import dataclass as py_dataclass

from nimbus.models.base import AuditMixinPy


@py_dataclass
class UserPy(AuditMixinPy):
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    extra_details: Dict


@py_dataclass
class UserMasterPy(AuditMixinPy):
    user_id: int
    mobile: str


class ProductsPy(AuditMixinPy):
    item_id: int
    item_name: str
    item_description: dict
    measure: str


class MerchantPy(AuditMixinPy):
    merchant_id: int
    email: str
    extra_details: Dict


class MerchantProduct(AuditMixinPy):
    merchant_id: int
    product_id: int
    status: str
    price: Decimal
