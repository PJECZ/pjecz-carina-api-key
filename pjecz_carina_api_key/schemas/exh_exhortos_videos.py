"""
Exh Exhortos Videos v4, esquemas de pydantic
"""

from pydantic import BaseModel


class ExhExhortoVideoItem(BaseModel):
    """Esquema para recibir los metadatos de un video"""

    titulo: str
    descripcion: str
    fecha: str  # YYYY-MM-DD
    urlAcceso: str
