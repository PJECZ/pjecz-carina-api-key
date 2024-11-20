"""
Exh Exhortos Promociones v4, esquemas de pydantic
"""

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ExhExhortoPromocionIn(BaseModel):
    """Esquema para recibir promociones de exhortos"""


class ExhExhortoPromocionOut(OneBaseOut):
    """Esquema para entregar promociones de exhortos"""


class OneExhExhortoPromocionOut(OneBaseOut):
    """Esquema para entregar una promoción de exhorto"""

    data: ExhExhortoPromocionOut | None = None
