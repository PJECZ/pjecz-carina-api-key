"""
Exh Exhortos v4, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel

from carina.v4.exh_exhortos_archivos.schemas import ExhExhortoArchivoIn
from carina.v4.exh_exhortos_partes.schemas import ExhExhortoParteIn
from carina.v4.exh_exhortos_videos.schemas import ExhExhortoVideoIn
from lib.schemas_base import OneBaseOut


class ExhExhortoIn(BaseModel):
    """Esquema para recibir exhortos"""

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
    partes: list[ExhExhortoParteIn] | None = None
    fojas: int | None = None
    diasResponder: int | None = None
    tipoDiligenciacionNombre: str | None = None
    fechaOrigen: datetime | None = None
    observaciones: str | None = None
    archivos: list[ExhExhortoArchivoIn] | None = None


class ExhExhortoOut(ExhExhortoIn):
    """Esquema para entregar exhortos"""

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


class OneExhExhortoOut(OneBaseOut):
    """Esquema para entregar un exhorto"""

    data: ExhExhortoOut | None = None


class ExhExhortoConfirmacionDatosExhortoRecibidoOut(BaseModel):
    """Esquema para confirmar la recepción de un exhorto"""

    exhortoOrigenId: str | None = None
    fechaHora: datetime | None = None


class OneExhExhortoConfirmacionDatosExhortoRecibidoOut(OneBaseOut):
    """Esquema para entregar una confirmación de la recepción de un exhorto"""

    data: ExhExhortoConfirmacionDatosExhortoRecibidoOut | None = None


class ExhExhortoRecibirRespuestaIn(BaseModel):
    """Esquema para recibir la respuesta de un exhorto que el Juzgado envió previamente al PJ exhortante"""

    exhortoId: str | None = None
    respuestaOrigenId: str | None = None
    municipioTurnadoId: int | None = None
    areaTurnadoId: str | None = None
    areaTurnadoNombre: str | None = None
    numeroExhorto: str | None = None
    tipoDiligenciado: int | None = None
    observaciones: str | None = None
    archivos: list[ExhExhortoArchivoIn] | None = None
    videos: list[ExhExhortoVideoIn] | None = None


class ExhExhortoRecibirRespuestaOut(BaseModel):
    """Respuesta de la operacion Recibir Respuesta Exhorto"""

    exhortoId: str | None = None
    respuestaOrigenId: str | None = None
    fechaHora: datetime | None = None


class OneExhExhortoRecibirRespuestaOut(OneBaseOut):
    """Esquema para entregar la respuesta de la operacion Recibir Respuesta Exhorto"""

    data: ExhExhortoRecibirRespuestaOut | None = None
