"""
Exh Exhortos Partes v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class ExhExhortoParte(BaseModel):
    """Esquema para estructurar el listado de partes"""

    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str
    genero: str
    esPersonaMoral: bool
    tipoParte: int
    tipoParteNombre: str


class ExhExhortoParteOut(ExhExhortoParte):
    """Esquema para entregar partes"""

    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoParteOut(OneBaseOut):
    """Esquema para entregar una parte"""

    data: ExhExhortoParteOut | None = None
