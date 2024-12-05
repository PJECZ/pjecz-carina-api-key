"""
Exh Exhortos Videos v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ExhExhortoVideoIn(BaseModel):
    """Esquema para recibir un video"""

    titulo: str | None = None
    descripcion: str | None = None
    fecha: str | None = None
    urlAcceso: str | None = None


class ExhExhortoVideoOut(ExhExhortoVideoIn):
    """Esquema para entregar videos"""

    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoVideoOut(OneBaseOut):
    """Esquema para entregar un video"""

    data: ExhExhortoVideoOut | None = None
