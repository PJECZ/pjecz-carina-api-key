"""
Exh Exhortos Promociones Promoventes v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ExhExhortoPromocionPromoventeIn(BaseModel):
    """Esquema para recibir promoventes de promociones"""

    nombre: str | None = None
    apellidoPaterno: str | None = None
    apellidoMaterno: str | None = None
    genero: str | None = None
    esPersonaMoral: bool | None = None
    tipoParte: int | None = None
    tipoParteNombre: str | None = None


class ExhExhortoPromocionPromoventeOut(ExhExhortoPromocionPromoventeIn):
    """Esquema para confirmar la recepción de un promovente de promoción"""

    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoPromocionPromoventeOut(OneBaseOut):
    """Esquema para entregar la confirmación de la recepción de un promovente de promoción"""

    data: ExhExhortoPromocionPromoventeOut | None = None
