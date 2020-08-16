from typing import Dict

from pendulum import DateTime
from pydantic import EmailStr
from pydantic.dataclasses import dataclass as py_dataclass


@py_dataclass
class AuditMixinPy:
    id: int
    performed_by: int
    created_at: DateTime
    updated_at: DateTime
    performed_by: int


@py_dataclass
class UserPy(AuditMixinPy):
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    extra_details: Dict
