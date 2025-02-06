"""
Materias v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class MateriaOut(BaseModel):
    """Esquema para entregar materias"""

    clave: str
    nombre: str
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneMateriaOut(OneBaseOut):
    """Esquema para entregar un materia"""

    data: MateriaOut | None = None
