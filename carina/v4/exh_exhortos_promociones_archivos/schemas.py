"""
Exh Exhortos Promociones Archivos v4, esquemas de pydantic
"""

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ExhExhortoPromocionArchivoIn(BaseModel):
    """Esquema para recibir archivos de promociones de exhortos"""


class ExhExhortoPromocionArchivoOut(OneBaseOut):
    """Esquema para entregar archivos de promociones de exhortos"""


class OneExhExhortoPromocionArchivoOut(OneBaseOut):
    """Esquema para entregar un archivo de promoción de exhorto"""

    data: ExhExhortoPromocionArchivoOut | None = None
