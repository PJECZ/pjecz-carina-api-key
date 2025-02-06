"""
Schemas Base
"""

from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class OneBaseOut(BaseModel):
    """OneBaseOut"""

    success: bool
    message: str
    errors: list[str] | None = None
    data: list[T] | None = None
