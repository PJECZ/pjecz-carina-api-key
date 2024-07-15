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
    tamano: int | None = None


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


class OneExhExhortoArchivoFileOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoArchivoFileDataOut | None = None


class ExhExhortoArchivoRecibirRespuestaExhortoIn(BaseModel):
    """Petición que se va a hacer por cada archivo que se quiere enviar en la respuesta del Exhorto"""

    # Identificador el exhorto que se originó en el Poder Judicial exhortante y
    # que se envió en RecibirExhortoRequest como parte de los datos generales del Exhorto.
    # Obligatorio y string.
    exhortoId: str | None = None

    # Identificador propio del Poder Judicial exhortado con el que identifica la respuesta del exhorto.
    # Este dato puede ser un número consecutivo (ej "1", "2", "3"...), un GUID/UUID o
    # cualquier otro valor con que se identifique la respuesta. Obligatorio y string.
    respuestaOrigenId: str | None = None


class ExhExhortoArchivoRecibirRespuestaExhortoOut(ExhExhortoArchivoRecibirRespuestaExhortoIn):
    """Esquema para entregar archivos"""

    id: int | None = None


class ExhExhortoArchivoRecibirRespuestaExhortoDataAcuseOut(BaseModel):
    """Data Acuse"""

    # Identificador del Exhorto que se orignió en el Poder Judicial exhortante,
    # el que el Poder Judicial exhortado recibió en RecibirExhortoRequest.exhortoOrigenId
    exhortoId: str | None = None

    # Identificador de la respuesta del Exhorto que el Poder Judicial exhortado genera y
    # con el que identifica el registro de la respuesta del Exhorto enviada o a enviar
    respuestaOrigenId: str | None = None

    # Fecha hora local en el que el Poder Judicial exhortante marca la Respuesta del Exhorto como recibida
    fechaHoraRecepcion: datetime | None = None


class ExhExhortoArchivoRecibirRespuestaExhortoDataOut(BaseModel):
    """Respuesta de la operación de Recibir Respuesta Exhorto Archivo"""

    # Contiene los datos del archivo recibido en el proceso
    archivo: ExhExhortoArchivoIn | None = None

    # Acuse de recepción de la Respuesta del Exhorto.
    # Este dato se envía cuando se recibe el último archivo de la respuesta del exhorto;
    # si todavía no se han subido todos los archivos, este dato se regresa como null.
    acuse: ExhExhortoArchivoRecibirRespuestaExhortoDataAcuseOut | None = None


class OneExhExhortoArchivoRecibirRespuestaExhortoOut(OneBaseOut):
    """Respuesta de la operación de Recibir Respuesta Exhorto Archivo"""

    data: ExhExhortoArchivoRecibirRespuestaExhortoDataOut | None = None
