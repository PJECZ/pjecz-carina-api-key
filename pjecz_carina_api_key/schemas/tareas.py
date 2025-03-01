"""
Tareas, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class TareaOut(BaseModel):
    """Esquema para entregar tareas"""

    id: str  # El ID es string y es el mismo que usa el RQ worker
    usuario_id: int
    usuario_email: str
    comando: str
    mensaje: str
    ha_terminado: bool
    model_config = ConfigDict(from_attributes=True)


class OneTareaOut(OneBaseOut):
    """Esquema para entregar un tarea"""

    data: TareaOut | None = None
