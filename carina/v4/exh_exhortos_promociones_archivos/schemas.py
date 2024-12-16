"""
Exh Exhortos Promociones Archivos v4, esquemas de pydantic
"""

from pydantic import BaseModel

from carina.v4.exh_exhortos_archivos.schemas import ExhExhortoArchivo
from lib.schemas_base import OneBaseOut


class ExhExhortoPromocionArchivo(BaseModel):
    """Esquema para estructurar el listado de archivos de una promoción"""

    nombreArchivo: str | None = None
    hashSha1: str | None = None
    hashSha256: str | None = None
    tipoDocumento: int | None = None


class ExhExhortoPromocionArchivoFileIn(BaseModel):
    """Esquema para recibir archivos Content-Disposition, form-data, file"""

    folioSeguimiento: str | None = None
    folioOrigenPromocion: str | None = None


class ExhExhortoPromocionArchivoDataAcuse(BaseModel):
    """Esquema con la estructura para la data con el acuse"""

    folioOrigenPromocion: str | None = None
    folioPromocionRecibida: str | None = None
    fechaHoraRecepcion: str | None = None  # YYYY-MM-DD HH:mm:ss


class ExhExhortoPromocionArchivoOut(BaseModel):
    """Esquema para entregar la confirmación de la recepción de un archivo de promoción"""

    archivo: ExhExhortoArchivo | None = None
    acuse: ExhExhortoPromocionArchivoDataAcuse | None = None


class OneExhExhortoPromocionArchivoOut(OneBaseOut):
    """Esquema para responder por un archivo recibido"""

    data: ExhExhortoPromocionArchivoOut | None = None
