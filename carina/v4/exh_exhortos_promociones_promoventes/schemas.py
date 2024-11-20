"""
Exh Exhortos Promociones Promoventes v4, esquemas de pydantic
"""

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ExhExhortoPromocionPromoventeIn(BaseModel):
    """Esquema para recibir promoventes de promociones de exhortos"""


class ExhExhortoPromocionPromoventeOut(OneBaseOut):
    """Esquema para entregar promoventes de promociones de exhortos"""


class OneExhExhortoPromocionPromoventeOut(OneBaseOut):
    """Esquema para entregar un promovente de promoción de exhorto"""

    data: ExhExhortoPromocionPromoventeOut | None = None
