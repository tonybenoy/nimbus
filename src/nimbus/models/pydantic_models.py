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


@py_dataclass
class ProductsPy(AuditMixinPy):
    item_id: int
    item_name: str
    item_description: dict
    measure: str


@py_dataclass
class MerchantPy(AuditMixinPy):
    merchant_id: int
    email: str
    extra_details: Dict


@py_dataclass
class MerchantProduct(AuditMixinPy):
    merchant_id: int
    product_id: int
    status: str
    price: Decimal


@py_dataclass
class OrderPy(AuditMixinPy):
    order_id: int
    merchant_id: int
    user_id: int
    status: str
    total: Decimal
    tax: Decimal
    gross: Decimal
    discount: Decimal
    extra_details: Dict


@py_dataclass
class OrderLinesPy(AuditMixinPy):
    order_id: int
    product_id: int
    quantity: Decimal
    status: str
    discount: Decimal
    price: Decimal
    extra_details: Dict
