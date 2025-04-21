"""
Exh Tipos Diligencias, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class ExhTipoDiligenciaOut(BaseModel):
    """Esquema para entregar areas"""

    clave: str
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneExhTipoDiligenciaOut(OneBaseOut):
    """Esquema para entregar un area"""

    data: ExhTipoDiligenciaOut | None = None
