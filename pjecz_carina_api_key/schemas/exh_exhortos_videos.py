"""
Exh Exhortos Videos v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class ExhExhortoVideoIn(BaseModel):
    """Esquema para estructurar el listado de videos de una promoción"""

    titulo: str
    descripcion: str
    fecha: str  # YYYY-MM-DD
    urlAcceso: str


class ExhExhortoVideoOut(ExhExhortoVideoIn):
    """Esquema para entregar videos de una promoción"""

    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoVideoOut(OneBaseOut):
    """Esquema para entregar un video de una promoción"""

    data: ExhExhortoVideoOut | None = None
