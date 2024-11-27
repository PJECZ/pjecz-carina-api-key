"""
Exh Exhortos Promociones v4, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from carina.v4.exh_exhortos_promociones_archivos.schemas import ExhExhortoPromocionArchivoIn
from carina.v4.exh_exhortos_promociones_promoventes.schemas import ExhExhortoPromocionPromoventeIn
from lib.schemas_base import OneBaseOut


class ExhExhortoPromocionIn(BaseModel):
    """Esquema para recibir promociones"""

    folioSeguimiento: str | None = None
    folioOrigenPromocion: str | None = None
    promoventes: list[ExhExhortoPromocionPromoventeIn] | None = None
    fojas: int | None = None
    fechaOrigen: datetime | None = None
    observaciones: str | None = None
    archivos: list[ExhExhortoPromocionArchivoIn] | None = None


class ExhExhortoPromocionOut(ExhExhortoPromocionIn):
    """Esquema para entregar promociones"""

    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoPromocionOut(OneBaseOut):
    """Esquema para entregar una promoción de exhorto"""

    data: ExhExhortoPromocionOut | None = None


class ExhExhortoPromocionConfirmacionOut(BaseModel):
    folioOrigenPromocion: str | None = None
    fechaHora: datetime | None = None


class OneExhExhortoPromocionConfirmacionOut(OneBaseOut):
    data: ExhExhortoPromocionConfirmacionOut | None = None
