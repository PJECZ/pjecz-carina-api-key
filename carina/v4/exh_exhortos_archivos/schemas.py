"""
Exh Exhortos Archivos v4, esquemas de pydantic
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ExhExhortoArchivoIn(BaseModel):
    """Esquema para recibir archivos"""

    nombreArchivo: str | None = None
    hashSha1: str | None = None
    hashSha256: str | None = None
    tipoDocumento: int | None = None


class ExhExhortoArchivoOut(ExhExhortoArchivoIn):
    """Esquema para entregar archivos"""

    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoArchivoOut(OneBaseOut):
    """Esquema para entregar un archivo"""

    data: ExhExhortoArchivoOut | None = None


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


class ExhExhortoArchivoFileOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoArchivoFileDataOut | None = None
