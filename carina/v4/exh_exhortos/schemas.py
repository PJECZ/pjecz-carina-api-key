"""
Exh Exhortos v4, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel

from carina.v4.exh_exhortos_archivos.schemas import ExhExhortoArchivo
from carina.v4.exh_exhortos_partes.schemas import ExhExhortoParte
from carina.v4.exh_exhortos_videos.schemas import ExhExhortoVideoIn
from lib.schemas_base import OneBaseOut


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
    fechaOrigen: datetime | None = None
    observaciones: str | None = None
    archivos: list[ExhExhortoArchivo] | None = None


class ExhExhortoOut(BaseModel):
    """Esquema para confirmar la recepción de un exhorto"""

    exhortoOrigenId: str | None = None
    fechaHora: datetime | None = None


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
    fechaHoraRecepcion: datetime | None = None
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
    fechaHora: datetime | None = None


class OneExhExhortoRespuestaOut(OneBaseOut):
    """Esquema para entregar la confirmación de la recepción de la respuesta"""

    data: ExhExhortoRespuestaOut | None = None
