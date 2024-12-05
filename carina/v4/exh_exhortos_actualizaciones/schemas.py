"""
Exh Exhortos Actualizaciones v4, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ExhExhortoActualizacionIn(BaseModel):
    """Esquema para recibir una actualización"""

    exhortoId: str | None = None
    actualizacionOrigenId: str | None = None
    tipoActualizacion: str | None = None
    fechaHora: str | None = None
    descripcion: str | None = None


class ExhExhortoActualizacionOut(BaseModel):
    """Esquema para confirmar la recepción de una actualización"""

    exhortoId: str | None = None
    actualizacionOrigenId: str | None = None
    fechaHora: datetime | None = None


class OneExhExhortoActualizacionOut(OneBaseOut):
    """Esquema para entregar la confirmación de la recepción de una actualización"""

    data: ExhExhortoActualizacionOut | None = None
