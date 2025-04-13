"""
Exh Exhortos Promoventes, esquemas de pydantic
"""

from pydantic import BaseModel


class ExhExhortoPromoventeItem(BaseModel):
    """Esquema para recibir los metadatos de un promovente"""

    nombre: str
    apellidoPaterno: str | None
    apellidoMaterno: str | None
    genero: str | None
    esPersonaMoral: bool
    tipoParte: int
    tipoParteNombre: str | None
    correoElectronico: str | None
    telefono: str | None
