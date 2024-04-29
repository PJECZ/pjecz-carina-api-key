"""
Exh Exhortos Archivos v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ExhExhortoArchivoOut(BaseModel):
    """Esquema para entregar archivos"""

    id: int | None = None
    exh_exhorto_id: int | None = None
    exh_exhorto_exhorto_origen_id: str | None = None
    nombre_archivo: str | None = None
    hash_sha1: str | None = None
    hash_sha256: str | None = None
    tipo_documento: int | None = None
    url: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoArchivoOut(ExhExhortoArchivoOut, OneBaseOut):
    """Esquema para entregar un archivo"""
