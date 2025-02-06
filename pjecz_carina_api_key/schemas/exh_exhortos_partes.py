"""
Exh Exhortos Partes v4, esquemas de pydantic
"""

from pydantic import BaseModel


class ExhExhortoParteItem(BaseModel):
    """Esquema para recibir los metadatos de una parte"""

    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str
    genero: str
    esPersonaMoral: bool
    tipoParte: int
    tipoParteNombre: str
