"""
Exh Exhortos Partes v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class ExhExhortoParte(BaseModel):
    """Esquema para estructurar el listado de partes"""

    nombre: str | None = None
    apellidoPaterno: str | None = None
    apellidoMaterno: str | None = None
    genero: str | None = None
    esPersonaMoral: bool | None = None
    tipoParte: int | None = None
    tipoParteNombre: str | None = None


class ExhExhortoParteOut(ExhExhortoParte):
    """Esquema para entregar partes"""

    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoParteOut(OneBaseOut):
    """Esquema para entregar una parte"""

    data: ExhExhortoParteOut | None = None
