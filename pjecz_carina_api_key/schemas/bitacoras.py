"""
Bitácoras v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class BitacoraOut(BaseModel):
    """Esquema para entregar bitacoras"""

    id: int
    modulo_id: int
    modulo_nombre: str
    usuario_id: int
    usuario_email: str
    descripcion: str
    url: str
    model_config = ConfigDict(from_attributes=True)


class OneBitacoraOut(OneBaseOut):
    """Esquema para entregar un bitacora"""

    data: BitacoraOut | None = None
