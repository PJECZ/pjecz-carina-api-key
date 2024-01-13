"""
Schemas Base
"""
from pydantic import BaseModel


class OneBaseOut(BaseModel):
    """OneBaseOut"""

    success: bool = True
    message: str = "Success"
