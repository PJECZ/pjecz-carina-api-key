"""
Exh Exhortos v4, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut
from .exh_exhortos_archivos import ExhExhortoArchivo
from .exh_exhortos_partes import ExhExhortoParte
from .exh_exhortos_videos import ExhExhortoVideoIn


class ExhExhortoIn(BaseModel):
    """Esquema para recibir un exhorto"""

    exhortoOrigenId: str | None = None
    municipioDestinoId: int | None = None
    materiaClave: str | None = None
    estadoOrigenId: int | None = None
    municipioOrigenId: int | None = None
    juzgadoOrigenId: str | None = None
    juzgadoOrigenNombre: str | None = None
    numeroExpedienteOrigen: str | None = None
    numeroOficioOrigen: str | None = None
    tipoJuicioAsuntoDelitos: str | None = None
    juezExhortante: str | None = None
    partes: list[ExhExhortoParte] | None = None
    fojas: int | None = None
    diasResponder: int | None = None
    tipoDiligenciacionNombre: str | None = None
    fechaOrigen: str | None = None  # YYYY-MM-DD HH:mm:ss
    observaciones: str | None = None
    archivos: list[ExhExhortoArchivo] | None = None


class ExhExhortoOut(BaseModel):
    """Esquema para confirmar la recepción de un exhorto"""

    exhortoOrigenId: str | None = None
    fechaHora: str | None = None  # YYYY-MM-DD HH:mm:ss


class OneExhExhortoOut(OneBaseOut):
    """Esquema para entregar una confirmación de la recepción de un exhorto"""

    data: ExhExhortoOut | None = None


class ExhExhortoConsultaOut(ExhExhortoIn):
    """Esquema para consultar un exhorto"""

    folioSeguimiento: str | None = None
    estadoDestinoId: int | None = None
    estadoDestinoNombre: str | None = None
    municipioDestinoNombre: str | None = None
    materiaNombre: str | None = None
    estadoOrigenNombre: str | None = None
    municipioOrigenNombre: str | None = None
    fechaHoraRecepcion: str | None = None  # YYYY-MM-DD HH:mm:ss
    municipioTurnadoId: int | None = None
    municipioTurnadoNombre: str | None = None
    areaTurnadoId: str | None = None
    areaTurnadoNombre: str | None = None
    numeroExhorto: str | None = None
    urlInfo: str | None = None
    respuestaOrigenId: str | None = None


class OneExhExhortoConsultaOut(OneBaseOut):
    """Esquema para entregar la consulta de un exhorto"""

    data: ExhExhortoConsultaOut | None = None


class ExhExhortoRespuestaIn(BaseModel):
    """Esquema para recibir la respuesta"""

    exhortoId: str | None = None
    respuestaOrigenId: str | None = None
    municipioTurnadoId: int | None = None
    areaTurnadoId: str | None = None
    areaTurnadoNombre: str | None = None
    numeroExhorto: str | None = None
    tipoDiligenciado: int | None = None  # 0 = No Diligenciado, 1 = Parcialmente Dilgenciado, 2 = Diligenciado
    observaciones: str | None = None
    archivos: list[ExhExhortoArchivo] | None = None
    videos: list[ExhExhortoVideoIn] | None = None


class ExhExhortoRespuestaOut(BaseModel):
    """Esquema para confirmar la recepción de la respuesta"""

    exhortoId: str | None = None
    respuestaOrigenId: str | None = None
    fechaHora: str | None = None  # YYYY-MM-DD HH:mm:ss


class OneExhExhortoRespuestaOut(OneBaseOut):
    """Esquema para entregar la confirmación de la recepción de la respuesta"""

    data: ExhExhortoRespuestaOut | None = None
