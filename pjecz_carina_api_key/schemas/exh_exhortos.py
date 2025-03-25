"""
Exh Exhortos, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut
from .exh_exhortos_archivos import ExhExhortoArchivoItem
from .exh_exhortos_partes import ExhExhortoParteItem


class ExhExhortoIn(BaseModel):
    """Esquema para recibir un exhorto"""

    exhortoOrigenId: str
    municipioDestinoId: int
    materiaClave: str
    estadoOrigenId: int
    municipioOrigenId: int
    juzgadoOrigenId: str | None
    juzgadoOrigenNombre: str
    numeroExpedienteOrigen: str
    numeroOficioOrigen: str | None
    tipoJuicioAsuntoDelitos: str
    juezExhortante: str | None
    partes: list[ExhExhortoParteItem] | None
    fojas: int
    diasResponder: int
    tipoDiligenciacionNombre: str | None
    fechaOrigen: str | None  # YYYY-MM-DD HH:mm:ss
    observaciones: str | None
    archivos: list[ExhExhortoArchivoItem]


class ExhExhortoOut(BaseModel):
    """Esquema para confirmar la recepción de un exhorto"""

    exhortoOrigenId: str
    fechaHora: str  # YYYY-MM-DD HH:mm:ss


class OneExhExhortoOut(OneBaseOut):
    """Esquema para entregar una confirmación de la recepción de un exhorto"""

    data: ExhExhortoOut | None = None


class ExhExhortoConsultaOut(BaseModel):
    """Esquema para consultar un exhorto"""

    exhortoOrigenId: str
    folioSeguimiento: str
    estadoDestinoId: int
    estadoDestinoNombre: str
    municipioDestinoId: int
    municipioDestinoNombre: str
    materiaClave: str
    materiaNombre: str
    estadoOrigenId: int
    estadoOrigenNombre: str
    municipioOrigenId: int
    municipioOrigenNombre: str
    juzgadoOrigenId: str | None
    juzgadoOrigenNombre: str
    numeroExpedienteOrigen: str
    numeroOficioOrigen: str | None
    tipoJuicioAsuntoDelitos: str
    juezExhortante: str | None
    partes: list[ExhExhortoParteItem] | None
    fojas: int
    diasResponder: int
    tipoDiligenciacionNombre: str | None
    fechaOrigen: str | None  # YYYY-MM-DD HH:mm:ss
    observaciones: str | None
    archivos: list[ExhExhortoArchivoItem]
    fechaHoraRecepcion: str  # YYYY-MM-DD HH:mm:ss
    municipioTurnadoId: int | None
    municipioTurnadoNombre: str | None
    areaTurnadoId: str | None
    areaTurnadoNombre: str | None
    numeroExhorto: str | None
    urlInfo: str | None


class OneExhExhortoConsultaOut(OneBaseOut):
    """Esquema para entregar la consulta de un exhorto"""

    data: ExhExhortoConsultaOut | None = None
