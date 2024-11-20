"""
Exh Exhortos Actualizaciones v4, esquemas de pydantic
"""

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ExhExhortoActualizacionIn(BaseModel):
    """Esquema para recibir actualizaciones de exhortos"""


class ExhExhortoActualizacionOut(OneBaseOut):
    """Esquema para entregar actualizaciones de exhortos"""


class OneExhExhortoActualizacionOut(OneBaseOut):
    """Esquema para entregar una actualización de exhorto"""

    data: ExhExhortoActualizacionOut | None = None
