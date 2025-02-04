"""
Exh Exhortos Promociones Archivos v4, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut
from .exh_exhortos_archivos import ExhExhortoArchivo


class ExhExhortoPromocionArchivo(BaseModel):
    """Esquema para estructurar el listado de archivos de una promoción"""

    nombreArchivo: str
    hashSha1: str
    hashSha256: str
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
    """Esquema para entregar la confirmación de la recepción de un archivo de promoción"""

    archivo: ExhExhortoArchivo
    acuse: ExhExhortoPromocionArchivoDataAcuse


class OneExhExhortoPromocionArchivoOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoPromocionArchivoOut | None = None
