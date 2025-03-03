"""
Exh Exhortos Promociones, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut
from .exh_exhortos_promociones_archivos import ExhExhortoPromocionArchivoItem
from .exh_exhortos_promociones_promoventes import ExhExhortoPromocionPromoventeItem


class ExhExhortoPromocionIn(BaseModel):
    """Esquema para recibir una promoción"""

    folioSeguimiento: str
    folioOrigenPromocion: str
    promoventes: list[ExhExhortoPromocionPromoventeItem]
    fojas: int
    fechaOrigen: str | None  # YYYY-MM-DD HH:mm:ss
    observaciones: str | None
    archivos: list[ExhExhortoPromocionArchivoItem]


class ExhExhortoPromocionOut(BaseModel):
    """Esquema para confirmar la recepción de una promoción"""

    folioSeguimiento: str
    folioOrigenPromocion: str
    fechaHora: str  # YYYY-MM-DD HH:mm:ss


class OneExhExhortoPromocionOut(OneBaseOut):
    """Esquema para entregar la confirmación de la recepción de una promoción"""

    data: ExhExhortoPromocionOut | None = None
