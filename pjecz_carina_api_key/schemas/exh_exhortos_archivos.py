"""
Exh Exhortos Archivos v4, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut


class ExhExhortoArchivo(BaseModel):
    """Esquema para estructurar el listado de archivos"""

    nombreArchivo: str
    hashSha1: str
    hashSha256: str
    tipoDocumento: int


class ExhExhortoArchivoFileIn(BaseModel):
    """Esquema para recibir archivos Content-Disposition, form-data, file"""

    exhortoOrigenId: str


class ExhExhortoArchivoFileDataArchivo(BaseModel):
    """Esquema para estructurar los datos del archivo"""

    nombreArchivo: str
    tamaño: int


class ExhExhortoArchivoFileDataAcuse(BaseModel):
    """Esquema para estructurar los datos del acuse"""

    exhortoOrigenId: str
    folioSeguimiento: str
    fechaHoraRecepcion: str  # YYYY-MM-DD HH:mm:ss
    municipioAreaRecibeId: int
    areaRecibeId: str
    areaRecibeNombre: str
    urlInfo: str


class ExhExhortoArchivoOut(BaseModel):
    """Esquema con el data"""

    archivo: ExhExhortoArchivoFileDataArchivo
    acuse: ExhExhortoArchivoFileDataAcuse


class OneExhExhortoArchivoOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoArchivoOut | None = None


class ExhExhortoArchivoRespuestaFileIn(BaseModel):
    """Esquema para recibir archivos Content-Disposition, form-data, file"""

    exhortoId: str
    respuestaOrigenId: str


class ExhExhortoArchivoRespuestaDataAcuse(BaseModel):
    """Data Acuse"""

    exhortoId: str
    respuestaOrigenId: str
    fechaHoraRecepcion: str  # YYYY-MM-DD HH:mm:ss


class ExhExhortoArchivoRespuestaOut(BaseModel):
    """Respuesta de la operación de Recibir Respuesta Exhorto Archivo"""

    archivo: ExhExhortoArchivoFileDataArchivo
    acuse: ExhExhortoArchivoRespuestaDataAcuse


class OneExhExhortoArchivoRespuestaOut(OneBaseOut):
    """Respuesta de la operación de Recibir Respuesta Exhorto Archivo"""

    data: ExhExhortoArchivoRespuestaOut | None = None
