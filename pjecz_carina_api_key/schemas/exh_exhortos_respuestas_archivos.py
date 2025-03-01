"""
Exh Exhortos Respuestas Archivos, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut
from .exh_exhortos_archivos import ExhExhortoArchivoItem


class ExhExhortoRespuestaArchivo(BaseModel):
    """Esquema para estructurar el listado de archivos"""

    nombreArchivo: str
    hashSha1: str
    hashSha256: str
    tipoDocumento: int


class ExhExhortoRespuestaArchivoFileIn(BaseModel):
    """Esquema para recibir archivos Content-Disposition, form-data, file"""

    folioSeguimiento: str
    folioOrigenRespuesta: str


class ExhExhortoRespuestaArchivoDataAcuse(BaseModel):
    """Esquema con la estructura para la data con el acuse"""

    folioOrigenRespuesta: str
    folioRespuestaRecibida: str
    fechaHoraRecepcion: str  # YYYY-MM-DD HH:mm:ss


class ExhExhortoRespuestaArchivoOut(BaseModel):
    """Esquema para entregar la confirmación de la recepción de un archivo"""

    archivo: ExhExhortoArchivoItem
    acuse: ExhExhortoRespuestaArchivoDataAcuse | None = None


class OneExhExhortoRespuestaArchivoOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoRespuestaArchivoOut | None = None
