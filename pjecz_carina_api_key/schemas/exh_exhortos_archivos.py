"""
Exh Exhortos Archivos, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut


class ExhExhortoArchivoItem(BaseModel):
    """Esquema para recibir los metadatos de un archivo en la recepción del exhorto"""

    nombreArchivo: str
    hashSha1: str | None
    hashSha256: str | None
    tipoDocumento: int


class ExhExhortoArchivoFileDataArchivo(BaseModel):
    """Esquema para estructurar los datos del archivo"""

    nombreArchivo: str
    tamaño: int


class ExhExhortoArchivoFileDataAcuse(BaseModel):
    """Esquema para estructurar los datos del acuse"""

    exhortoOrigenId: str
    folioSeguimiento: str
    fechaHoraRecepcion: str  # YYYY-MM-DD HH:mm:ss
    municipioAreaRecibeId: int | None
    areaRecibeId: str | None
    areaRecibeNombre: str | None
    urlInfo: str | None


class ExhExhortoArchivoOut(BaseModel):
    """Esquema con el data"""

    archivo: ExhExhortoArchivoFileDataArchivo
    acuse: ExhExhortoArchivoFileDataAcuse | None = None


class OneExhExhortoArchivoOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoArchivoOut | None = None
