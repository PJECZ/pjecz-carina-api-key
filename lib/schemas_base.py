"""
Schemas Base
"""

from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class OneBaseOut(BaseModel):
    """OneBaseOut"""

    success: bool = True
    message: str = "Success"
    errors: list[str]
    data: list[T]
