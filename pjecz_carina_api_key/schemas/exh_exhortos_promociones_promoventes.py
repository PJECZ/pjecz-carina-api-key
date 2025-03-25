"""
Exh Exhortos Promociones Promoventes, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class ExhExhortoPromocionPromoventeItem(BaseModel):
    """Esquema para estructurar el listado de promoventes"""

    nombre: str
    apellidoPaterno: str | None
    apellidoMaterno: str | None
    genero: str | None
    esPersonaMoral: bool
    tipoParte: int
    tipoParteNombre: str | None
