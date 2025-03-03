"""
Exh Exhortos Respuestas Archivos, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut


class ExhExhortoRespuestaArchivoItem(BaseModel):
    """Esquema para recibir los metadatos de un archivo en la recepción de una respuesta"""

    nombreArchivo: str
    hashSha1: str | None
    hashSha256: str | None
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

    archivo: ExhExhortoRespuestaArchivoItem
    acuse: ExhExhortoRespuestaArchivoDataAcuse | None = None


class OneExhExhortoRespuestaArchivoOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoRespuestaArchivoOut | None = None
