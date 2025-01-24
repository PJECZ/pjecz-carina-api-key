"""
Exh Externos v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class ExhExternoOut(BaseModel):
    """Esquema para entregar externos"""

    clave: str | None = None
    descripcion: str | None = None
    materias: dict | None = None
    endpoint_consultar_materias: str | None = None
    endpoint_recibir_exhorto: str | None = None
    endpoint_recibir_exhorto_archivo: str | None = None
    endpoint_consultar_exhorto: str | None = None
    endpoint_recibir_respuesta_exhorto: str | None = None
    endpoint_recibir_respuesta_exhorto_archivo: str | None = None
    endpoint_actualizar_exhorto: str | None = None
    endpoint_recibir_promocion: str | None = None
    endpoint_recibir_promocion_archivo: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExternoOut(OneBaseOut):
    """Esquema para entregar un externo"""

    data: ExhExternoOut | None = None
