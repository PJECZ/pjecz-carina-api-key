"""
Exh Exhortos Promociones Archivos v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ExhExhortoPromocionArchivoIn(BaseModel):
    """Esquema para recibir archivos de promociones"""

    nombreArchivo: str | None = None
    hashSha1: str | None = None
    hashSha256: str | None = None
    tipoDocumento: int | None = None


class ExhExhortoPromocionArchivoOut(ExhExhortoPromocionArchivoIn):
    """Esquema para entregar archivos de promociones"""

    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoPromocionArchivoOut(OneBaseOut):
    """Esquema para entregar un archivo de promoción"""

    data: ExhExhortoPromocionArchivoOut | None = None
