"""
Bitácoras v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class BitacoraOut(BaseModel):
    """Esquema para entregar bitacoras"""

    id: int | None = None
    modulo_id: int | None = None
    modulo_nombre: str | None = None
    usuario_id: int | None = None
    usuario_email: str | None = None
    descripcion: str | None = None
    url: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneBitacoraOut(OneBaseOut):
    """Esquema para entregar un bitacora"""

    data: BitacoraOut | None = None
