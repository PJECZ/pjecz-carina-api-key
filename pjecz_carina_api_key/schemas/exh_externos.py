"""
Exh Externos v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class ExhExternoOut(BaseModel):
    """Esquema para entregar externos"""

    clave: str
    descripcion: str
    materias: dict
    endpoint_consultar_materias: str
    endpoint_recibir_exhorto: str
    endpoint_recibir_exhorto_archivo: str
    endpoint_consultar_exhorto: str
    endpoint_recibir_respuesta_exhorto: str
    endpoint_recibir_respuesta_exhorto_archivo: str
    endpoint_actualizar_exhorto: str
    endpoint_recibir_promocion: str
    endpoint_recibir_promocion_archivo: str
    model_config = ConfigDict(from_attributes=True)
