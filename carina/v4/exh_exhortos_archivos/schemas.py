"""
Exh Exhortos Archivos v4, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ExhExhortoArchivo(BaseModel):
    """Esquema para estructurar el listado de archivos de un exhorto"""

    nombreArchivo: str | None = None
    hashSha1: str | None = None
    hashSha256: str | None = None
    tipoDocumento: int | None = None


class ExhExhortoArchivoFileIn(BaseModel):
    """Esquema para recibir archivos Content-Disposition, form-data, file"""

    exhortoOrigenId: str | None = None


class ExhExhortoArchivoFileDataArchivo(BaseModel):
    """Esquema con datos del archivo"""

    nombreArchivo: str | None = None
    tamaño: int | None = None


class ExhExhortoArchivoFileDataAcuse(BaseModel):
    """Esquema con el acuse"""

    exhortoOrigenId: str | None = None
    folioSeguimiento: str | None = None
    fechaHoraRecepcion: datetime | None = None
    municipioAreaRecibeId: int | None = None
    areaRecibeId: str | None = None
    areaRecibeNombre: str | None = None
    urlInfo: str | None = None


class ExhExhortoArchivoFileDataOut(BaseModel):
    """Esquema con el data"""

    archivo: ExhExhortoArchivoFileDataArchivo | None = None
    acuse: ExhExhortoArchivoFileDataAcuse | None = None


class OneExhExhortoArchivoFileDataOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoArchivoFileDataOut | None = None


class ExhExhortoArchivoRespuestaIn(BaseModel):
    """Petición que se va a hacer por cada archivo que se quiere enviar en la respuesta del Exhorto"""

    exhortoId: str | None = None
    respuestaOrigenId: str | None = None


class ExhExhortoArchivoRespuestaDataAcuse(BaseModel):
    """Data Acuse"""

    exhortoId: str | None = None
    respuestaOrigenId: str | None = None
    fechaHoraRecepcion: datetime | None = None


class ExhExhortoArchivoRespuestaDataOut(BaseModel):
    """Respuesta de la operación de Recibir Respuesta Exhorto Archivo"""

    archivo: ExhExhortoArchivoFileDataArchivo | None = None
    acuse: ExhExhortoArchivoRespuestaDataAcuse | None = None


class OneExhExhortoArchivoRespuestaDataOut(OneBaseOut):
    """Respuesta de la operación de Recibir Respuesta Exhorto Archivo"""

    data: ExhExhortoArchivoRespuestaDataOut | None = None
