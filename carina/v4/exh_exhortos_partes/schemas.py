"""
Exh Exhortos Partes v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ExhExhortoParteIn(BaseModel):
    """Esquema para recibir partes"""

    nombre: str | None = None
    apellidoPaterno: str | None = None
    apellidoMaterno: str | None = None
    genero: str | None = None
    esPersonaMoral: bool | None = None
    tipoParte: int | None = None
    tipoParteNombre: str | None = None


class ExhExhortoParteOut(ExhExhortoParteIn):
    """Esquema para entregar partes"""

    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoParteOut(OneBaseOut):
    """Esquema para entregar un parte"""

    data: list[ExhExhortoParteOut] | None = None
