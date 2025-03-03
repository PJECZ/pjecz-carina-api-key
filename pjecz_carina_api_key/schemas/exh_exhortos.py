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


class ExhExhortoConsultaOut(ExhExhortoIn):
    """Esquema para consultar un exhorto"""

    folioSeguimiento: str
    estadoDestinoId: int
    estadoDestinoNombre: str
    municipioDestinoNombre: str
    materiaNombre: str
    estadoOrigenNombre: str
    municipioOrigenNombre: str
    fechaHoraRecepcion: str  # YYYY-MM-DD HH:mm:ss
    municipioTurnadoId: int
    municipioTurnadoNombre: str
    areaTurnadoId: str
    areaTurnadoNombre: str
    numeroExhorto: str
    urlInfo: str
    respuestaOrigenId: str


class OneExhExhortoConsultaOut(OneBaseOut):
    """Esquema para entregar la consulta de un exhorto"""

    data: ExhExhortoConsultaOut | None = None
