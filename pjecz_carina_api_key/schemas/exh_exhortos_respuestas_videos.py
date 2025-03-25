"""
Exh Exhortos Respuestas Videos, esquemas de pydantic
"""

from pydantic import BaseModel


class ExhExhortoRespuestaVideoItem(BaseModel):
    """Esquema para recibir los metadatos de un video"""

    titulo: str
    descripcion: str | None
    fecha: str | None  # YYYY-MM-DD
    urlAcceso: str
