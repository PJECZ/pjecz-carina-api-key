"""
Exh Exhortos Promociones v4, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from carina.v4.exh_exhortos_promociones_archivos.schemas import ExhExhortoPromocionArchivo
from carina.v4.exh_exhortos_promociones_promoventes.schemas import ExhExhortoPromocionPromoventeIn
from lib.schemas_base import OneBaseOut


class ExhExhortoPromocionIn(BaseModel):
    """Esquema para recibir una promoción"""

    folioSeguimiento: str | None = None
    folioOrigenPromocion: str | None = None
    promoventes: list[ExhExhortoPromocionPromoventeIn] | None = None
    fojas: int | None = None
    fechaOrigen: datetime | None = None
    observaciones: str | None = None
    archivos: list[ExhExhortoPromocionArchivo] | None = None


class ExhExhortoPromocionOut(ExhExhortoPromocionIn):
    """Esquema para confirmar la recepción de una promoción"""

    folioSeguimiento: str | None = None
    folioOrigenPromocion: str | None = None
    fechaHora: datetime | None = None


class OneExhExhortoPromocionOut(OneBaseOut):
    """Esquema para entregar una confirmación de recepción de una promoción"""

    data: ExhExhortoPromocionOut | None = None
