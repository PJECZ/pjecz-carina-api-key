"""
Exh Exhortos Promociones Promoventes, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class ExhExhortoPromocionPromovente(BaseModel):
    """Esquema para estructurar el listado de promoventes"""

    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str
    genero: str
    esPersonaMoral: bool
    tipoParte: int
    tipoParteNombre: str


class ExhExhortoPromocionPromoventeOut(ExhExhortoPromocionPromovente):
    """Esquema para entregar promoventes"""

    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoPromocionPromoventeOut(OneBaseOut):
    """Esquema para entregar un promovente"""

    data: ExhExhortoPromocionPromoventeOut | None = None
