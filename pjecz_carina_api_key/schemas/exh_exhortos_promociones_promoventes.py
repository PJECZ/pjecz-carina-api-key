"""
Exh Exhortos Promociones Promoventes v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class ExhExhortoPromocionPromovente(BaseModel):
    """Esquema para estructurar el listado de promoventes de una promoción"""

    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str
    genero: str
    esPersonaMoral: bool
    tipoParte: int
    tipoParteNombre: str


class ExhExhortoPromocionPromoventeOut(ExhExhortoPromocionPromovente):
    """Esquema para entregar promoventes de una promoción"""

    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoPromocionPromoventeOut(OneBaseOut):
    """Esquema para entregar un promovente de una promoción"""

    data: ExhExhortoPromocionPromoventeOut | None = None
