"""
Exh Exhortos Respuestas, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut
from .exh_exhortos_archivos import ExhExhortoArchivoItem
from .exh_exhortos_respuestas_videos import ExhExhortoVideoItem


class ExhExhortoRespuestaIn(BaseModel):
    """Esquema para recibir una respuesta"""

    exhortoId: str
    respuestaOrigenId: str
    municipioTurnadoId: int
    areaTurnadoId: str | None
    areaTurnadoNombre: str
    numeroExhorto: str | None
    tipoDiligenciado: int  # 0 = No Diligenciado, 1 = Parcialmente Dilgenciado, 2 = Diligenciado
    observaciones: str | None
    archivos: list[ExhExhortoArchivoItem]
    videos: list[ExhExhortoVideoItem] | None


class ExhExhortoRespuestaOut(BaseModel):
    """Esquema para confirmar la recepción de una respuesta"""

    folioSeguimiento: str
    folioOrigenRespuesta: str
    fechaHora: str  # YYYY-MM-DD HH:mm:ss


class OneExhExhortoRespuestaOut(OneBaseOut):
    """Esquema para entregar la confirmación de la recepción de una respuesta"""

    data: ExhExhortoRespuestaOut | None = None
