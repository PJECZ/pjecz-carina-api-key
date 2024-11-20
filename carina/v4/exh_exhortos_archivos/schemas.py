"""
Exh Exhortos Archivos v4, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ExhExhortoArchivoIn(BaseModel):
    """Esquema para recibir archivos"""

    nombreArchivo: str | None = None
    hashSha1: str | None = None
    hashSha256: str | None = None
    tipoDocumento: int | None = None


class ExhExhortoArchivoDataOut(ExhExhortoArchivoIn):
    """Esquema para entregar archivos"""

    id: int | None = None


class OneExhExhortoArchivoOut(OneBaseOut):
    """Esquema para entregar un archivo"""

    data: ExhExhortoArchivoDataOut | None = None


class ExhExhortoArchivoFileIn(BaseModel):
    """Exquema para recibir archivos Content-Disposition, form-data, file"""

    exhortoOrigenId: str | None = None


class ExhExhortoArchivoFileDataArchivoOut(BaseModel):
    """Esquema con datos adicionales del archivo"""

    nombreArchivo: str | None = None
    tamaño: int | None = None


class ExhExhortoArchivoFileDataAcuseOut(BaseModel):
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

    archivo: ExhExhortoArchivoFileDataArchivoOut | None = None
    acuse: ExhExhortoArchivoFileDataAcuseOut | None = None


class OneExhExhortoArchivoFileDataOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoArchivoFileDataOut | None = None


class ExhExhortoArchivoRecibirRespuestaExhortoIn(BaseModel):
    """Petición que se va a hacer por cada archivo que se quiere enviar en la respuesta del Exhorto"""

    exhortoId: str | None = None
    respuestaOrigenId: str | None = None


class ExhExhortoArchivoRecibirRespuestaExhortoOut(ExhExhortoArchivoRecibirRespuestaExhortoIn):
    """Esquema para entregar archivos"""

    id: int | None = None


class ExhExhortoArchivoRecibirRespuestaExhortoDataAcuseOut(BaseModel):
    """Data Acuse"""

    exhortoId: str | None = None
    respuestaOrigenId: str | None = None
    fechaHoraRecepcion: datetime | None = None


class ExhExhortoArchivoRecibirRespuestaExhortoDataOut(BaseModel):
    """Respuesta de la operación de Recibir Respuesta Exhorto Archivo"""

    archivo: ExhExhortoArchivoFileDataArchivoOut | None = None
    acuse: ExhExhortoArchivoRecibirRespuestaExhortoDataAcuseOut | None = None


class OneExhExhortoArchivoRecibirRespuestaExhortoOut(OneBaseOut):
    """Respuesta de la operación de Recibir Respuesta Exhorto Archivo"""

    data: ExhExhortoArchivoRecibirRespuestaExhortoDataOut | None = None
