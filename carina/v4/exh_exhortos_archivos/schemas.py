"""
Exh Exhortos Archivos v4, esquemas de pydantic
"""

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ExhExhortoArchivo(BaseModel):
    """Esquema para estructurar el listado de archivos"""

    nombreArchivo: str | None = None
    hashSha1: str | None = None
    hashSha256: str | None = None
    tipoDocumento: int | None = None


class ExhExhortoArchivoFileIn(BaseModel):
    """Esquema para recibir archivos Content-Disposition, form-data, file"""

    exhortoOrigenId: str | None = None


class ExhExhortoArchivoFileDataArchivo(BaseModel):
    """Esquema para estructurar los datos del archivo"""

    nombreArchivo: str | None = None
    tamaño: int | None = None


class ExhExhortoArchivoFileDataAcuse(BaseModel):
    """Esquema para estructurar los datos del acuse"""

    exhortoOrigenId: str | None = None
    folioSeguimiento: str | None = None
    fechaHoraRecepcion: str | None = None  # YYYY-MM-DD HH:mm:ss
    municipioAreaRecibeId: int | None = None
    areaRecibeId: str | None = None
    areaRecibeNombre: str | None = None
    urlInfo: str | None = None


class ExhExhortoArchivoOut(BaseModel):
    """Esquema con el data"""

    archivo: ExhExhortoArchivoFileDataArchivo | None = None
    acuse: ExhExhortoArchivoFileDataAcuse | None = None


class OneExhExhortoArchivoOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoArchivoOut | None = None


class ExhExhortoArchivoRespuestaFileIn(BaseModel):
    """Esquema para recibir archivos Content-Disposition, form-data, file"""

    exhortoId: str | None = None
    respuestaOrigenId: str | None = None


class ExhExhortoArchivoRespuestaDataAcuse(BaseModel):
    """Data Acuse"""

    exhortoId: str | None = None
    respuestaOrigenId: str | None = None
    fechaHoraRecepcion: str | None = None  # YYYY-MM-DD HH:mm:ss


class ExhExhortoArchivoRespuestaOut(BaseModel):
    """Respuesta de la operación de Recibir Respuesta Exhorto Archivo"""

    archivo: ExhExhortoArchivoFileDataArchivo | None = None
    acuse: ExhExhortoArchivoRespuestaDataAcuse | None = None


class OneExhExhortoArchivoRespuestaOut(OneBaseOut):
    """Respuesta de la operación de Recibir Respuesta Exhorto Archivo"""

    data: ExhExhortoArchivoRespuestaOut | None = None
