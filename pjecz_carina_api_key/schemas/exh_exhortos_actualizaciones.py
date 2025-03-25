"""
Exh Exhortos Actualizaciones, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut


class ExhExhortoActualizacionIn(BaseModel):
    """Esquema para recibir una actualización"""

    exhortoId: str
    actualizacionOrigenId: str
    tipoActualizacion: str
    fechaHora: str  # YYYY-MM-DD HH:mm:ss
    descripcion: str


class ExhExhortoActualizacionOut(BaseModel):
    """Esquema para confirmar la recepción de una actualización"""

    exhortoId: str
    actualizacionOrigenId: str
    fechaHora: str  # YYYY-MM-DD HH:mm:ss


class OneExhExhortoActualizacionOut(OneBaseOut):
    """Esquema para entregar la confirmación de la recepción de una actualización"""

    data: ExhExhortoActualizacionOut | None = None
