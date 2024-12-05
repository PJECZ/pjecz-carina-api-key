"""
Exh Exhortos Promociones Promoventes v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ExhExhortoPromocionPromovente(BaseModel):
    """Esquema para estructurar el listado de promoventes de una promoción"""

    nombre: str | None = None
    apellidoPaterno: str | None = None
    apellidoMaterno: str | None = None
    genero: str | None = None
    esPersonaMoral: bool | None = None
    tipoParte: int | None = None
    tipoParteNombre: str | None = None


class ExhExhortoPromocionPromoventeOut(ExhExhortoPromocionPromovente):
    """Esquema para entregar promoventes de una promoción"""

    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoPromocionPromoventeOut(OneBaseOut):
    """Esquema para entregar un promovente de una promoción"""

    data: ExhExhortoPromocionPromoventeOut | None = None
