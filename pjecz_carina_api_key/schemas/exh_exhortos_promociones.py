"""
Exh Exhortos Promociones v4, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut
from .exh_exhortos_promociones_archivos import ExhExhortoPromocionArchivo
from .exh_exhortos_promociones_promoventes import ExhExhortoPromocionPromovente


class ExhExhortoPromocionIn(BaseModel):
    """Esquema para recibir una promoción"""

    folioSeguimiento: str | None = None
    folioOrigenPromocion: str | None = None
    promoventes: list[ExhExhortoPromocionPromovente] | None = None
    fojas: int | None = None
    fechaOrigen: str | None = None  # YYYY-MM-DD HH:mm:ss
    observaciones: str | None = None
    archivos: list[ExhExhortoPromocionArchivo] | None = None


class ExhExhortoPromocionOut(BaseModel):
    """Esquema para confirmar la recepción de una promoción"""

    folioSeguimiento: str | None = None
    folioOrigenPromocion: str | None = None
    fechaHora: str | None = None  # YYYY-MM-DD HH:mm:ss


class OneExhExhortoPromocionOut(OneBaseOut):
    """Esquema para entregar la confirmación de la recepción de una promoción"""

    data: ExhExhortoPromocionOut | None = None
