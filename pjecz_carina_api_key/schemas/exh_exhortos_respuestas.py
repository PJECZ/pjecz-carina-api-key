"""
Exh Exhortos Respuestas, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut
from .exh_exhortos_respuestas_archivos import ExhExhortoRespuestaArchivoItem
from .exh_exhortos_respuestas_videos import ExhExhortoRespuestaVideoItem


class ExhExhortoRespuestaIn(BaseModel):
    """Esquema para recibir una respuesta"""

    exhortoId: str
    respuestaOrigenId: str
    municipioTurnadoId: int
    areaTurnadoId: str | None
    areaTurnadoNombre: str
    numeroExhorto: str | None
    tipoDiligenciado: int  # 0 = No Diligenciado, 1 = Parcialmente Diligenciado, 2 = Diligenciado
    observaciones: str | None
    archivos: list[ExhExhortoRespuestaArchivoItem]
    videos: list[ExhExhortoRespuestaVideoItem] | None


class ExhExhortoRespuestaOut(BaseModel):
    """Esquema para confirmar la recepción de una respuesta"""

    exhortoId: str
    respuestaOrigenId: str
    fechaHora: str  # YYYY-MM-DD HH:mm:ss


class OneExhExhortoRespuestaOut(OneBaseOut):
    """Esquema para entregar la confirmación de la recepción de una respuesta"""

    data: ExhExhortoRespuestaOut | None = None
