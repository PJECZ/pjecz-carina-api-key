"""
Exh Exhortos Partes v4, esquemas de pydantic
"""

from pydantic import BaseModel


class ExhExhortoParteOut(BaseModel):
    """Esquema para entregar partes"""

    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str
    genero: str
    esPersonaMoral: bool
    tipoParte: int
    tipoParteNombre: str
