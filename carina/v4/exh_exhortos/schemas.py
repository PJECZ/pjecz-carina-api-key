"""
Exh Exhortos v4, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut
from ..exh_exhortos_archivos.schemas import ExhExhortoArchivoIn
from ..exh_exhortos_partes.schemas import ExhExhortoParteIn


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

    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoOut(OneBaseOut):
    """Esquema para entregar un exhorto"""

    data: ExhExhortoOut | None = None


class ExhExhortoConfirmacionDatosExhortoRecibidoOut(BaseModel):
    """Esquema para confirmar la recepción de un exhorto"""

    id: int | None = None
    exhortoOrigenId: str | None = None
    fechaHora: datetime | None = None


class OneExhExhortoConfirmacionDatosExhortoRecibidoOut(OneBaseOut):
    """Esquema para entregar una confirmación de la recepción de un exhorto"""

    data: list[ExhExhortoConfirmacionDatosExhortoRecibidoOut] | None = None
