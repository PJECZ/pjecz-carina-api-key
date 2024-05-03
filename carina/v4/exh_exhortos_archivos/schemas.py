"""
Exh Exhortos Archivos v4, esquemas de pydantic
"""

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
