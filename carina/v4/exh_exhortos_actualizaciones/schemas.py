"""
Exh Exhortos Actualizaciones v4, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ExhExhortoActualizacionIn(BaseModel):
    """Esquema para recibir actualizaciones"""

    exhortoId: str | None = None
    actualizacionOrigenId: str | None = None
    tipoActualizacion: str | None = None
    fechaHora: datetime | None = None
    descripcion: str | None = None


class ExhExhortoActualizacionOut(ExhExhortoActualizacionIn):
    """Esquema para entregar actualizaciones"""

    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoActualizacionOut(OneBaseOut):
    """Esquema para entregar una actualización"""

    data: ExhExhortoActualizacionOut | None = None


class ExhExhortoConfirmacionActualizacionOut(BaseModel):
    """Esquema para entregar la respuesta a la actualización"""

    exhortoId: str | None = None
    actualizacionOrigenId: str | None = None
    fechaHora: datetime | None = None


class OneExhExhortoConfirmacionActualizacionOut(OneBaseOut):
    """Esquema para entregar la respuesta a la actualización"""

    data: ExhExhortoConfirmacionActualizacionOut | None = None
