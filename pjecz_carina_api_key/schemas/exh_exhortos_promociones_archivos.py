"""
Exh Exhortos Promociones Archivos, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut


class ExhExhortoPromocionArchivoItem(BaseModel):
    """Esquema para recibir los metadatos de un archivo en la recepción de una promoción"""

    nombreArchivo: str
    hashSha1: str | None
    hashSha256: str | None
    tipoDocumento: int


class ExhExhortoPromocionArchivoFileIn(BaseModel):
    """Esquema para recibir archivos Content-Disposition, form-data, file"""

    folioSeguimiento: str
    folioOrigenPromocion: str


class ExhExhortoPromocionArchivoDataAcuse(BaseModel):
    """Esquema con la estructura para la data con el acuse"""

    folioOrigenPromocion: str
    folioPromocionRecibida: str
    fechaHoraRecepcion: str  # YYYY-MM-DD HH:mm:ss


class ExhExhortoPromocionArchivoOut(BaseModel):
    """Esquema para entregar la confirmación de la recepción de un archivo"""

    archivo: ExhExhortoPromocionArchivoItem
    acuse: ExhExhortoPromocionArchivoDataAcuse | None = None


class OneExhExhortoPromocionArchivoOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoPromocionArchivoOut | None = None
