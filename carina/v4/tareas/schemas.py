"""
Tareas v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class TareaOut(BaseModel):
    """Esquema para entregar tareas"""

    id: str | None = None  # El id es string y es el mismo que usa el RQ worker
    usuario_id: int | None = None
    usuario_email: str | None = None
    comando: str | None = None
    mensaje: str | None = None
    ha_terminado: bool | None = None
    model_config = ConfigDict(from_attributes=True)


class OneTareaOut(TareaOut, OneBaseOut):
    """Esquema para entregar un tarea"""
