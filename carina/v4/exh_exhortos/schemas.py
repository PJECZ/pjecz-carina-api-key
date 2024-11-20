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

    # exhortoOrigenId: Es el identificador con el que el Poder Judicial exhortante identifica el exhorto que envía.
    # Este dato puede ser un número consecutivo si así el Poder Judicial exhortante (de origen) identifica
    # el registro del Exhorto, también puede ser un GUID/UUID u otro valor que sea único para el Poder Judicial exhortante.
    # Este dato es importante porque se utilizará para poder hacer la devolución/respuesta del exhorto por el Juzgado exhortado.
    exhortoOrigenId: str | None = None

    # municipioDestinoId: Identificador del municipio del Estado del Poder Judical exhortado al que se quiere enviar el Exhorto.
    # Este debe corresponder al identificador definido por el catálogo de municipios y estados del INEGI
    municipioDestinoId: str | None = None

    # materiaClave	string	SI	Clave de la materia (el que se obtuvo en la consulta de materias del Poder Judicial exhortado)
    # al que el Exhorto hace referencia. Este contiene la materia actuál del registro del Exhorto
    materiaClave: str | None = None

    # estadoOrigenId: Identificador del estado de origen del municipio donde se ubica el Juzgado del Poder Judicial exhortante.
    # Este dato debe ser uno de los valores correspondientes al catálogo de estados del INEGI.
    estadoOrigenId: int | None = None

    # municipioOrigenId	int	SI	Identificador del municipio donde está localizado el Juzgado/Área del Poder Judicial exhortante.
    # Este identificador debe coincidir con el del catálogo del INEGI de municipios y estados.
    municipioOrigenId: int | None = None

    # juzgadoOrigenId: Identificador propio del Juzgado/Área que envía el Exhorto.
    # Identificador con el que el Poder Judicial exhortante identifica al Juzgado/Área
    juzgadoOrigenId: str | None = None

    # juzgadoOrigenNombre: Nombre del Juzgado/Área que envía el Exhorto.
    juzgadoOrigenNombre: str | None = None

    # numeroExpedienteOrigen: El número de expediente (o carpeta procesal, carpeta...)
    # que tiene el asunto en el Juzgado de Origen.
    numeroExpedienteOrigen: str | None = None

    # numeroOficioOrigen: El número del oficio con el que se envía el exhorto,
    # el que corresponde al control interno del Juzgado de origen
    numeroOficioOrigen: str | None = None

    # tipoJuicioAsuntoDelitos: Nombre del tipo de Juicio, o asunto, listado de los delitos (para materia Penal)
    # que corresponde al Expediente del cual el Juzgado envía el Exhorto
    tipoJuicioAsuntoDelitos: str | None = None

    # juezExhortante: Nombre completo del Juez del Juzgado o titular del Área que envía el Exhorto
    juezExhortante: str | None = None

    # partes: Contiene la definición de las partes del Expediente
    partes: list[ExhExhortoParteIn] | None = None

    # fojas: Número de fojas que contiene el exhorto. El valor 0 significa "No Especificado".
    fojas: int | None = None

    # diasResponder: Cantidad de dias a partir del día que se recibió en el Poder Judicial exhortado que se tiene para
    # responder el Exhorto. El valor de 0 significa "No Especificado".
    diasResponder: int | None = None

    # tipoDiligenciacionNombre: Nombre del tipo de diligenciación que le corresponde al exhorto enviado.
    # Este puede contener valores como "Oficio", "Petición de Parte"
    tipoDiligenciacionNombre: str | None = None

    # fechaOrigen: Fecha y hora en que el Poder Judicial exhortante registró que se envió el exhorto en su hora local.
    # En caso de no enviar este dato, el Poder Judicial exhortado puede tomar su fecha hora local.
    fechaOrigen: datetime | None = None

    # observaciones: Texto simple que contenga información extra o relevante sobre el exhorto.
    observaciones: str | None = None

    # archivos: Colección de los datos correspondientes a los archivos recibidos del Exhorto
    archivos: list[ExhExhortoArchivoIn] | None = None


class ExhExhortoOut(ExhExhortoIn):
    """Esquema para entregar exhortos"""

    # folioSeguimiento: Folio de seguimiento generado para el Exhorto que recibió el Poder Judicial Exhortado
    folioSeguimiento: str | None = None

    # estadoDestinoId: Identificador del estado de destino del Exhorto
    estadoDestinoId: int | None = None

    # estadoDestinoNombre: Nombre del estado de destino del Exhorto
    estadoDestinoNombre: str | None = None

    # municipioDestinoNombre: Nombre del municipio de destino al que se envió el Exhorto
    municipioDestinoNombre: str | None = None

    # materiaNombre: Nombre de la materia
    materiaNombre: str | None = None

    # estadoOrigenNombre: Nombre del Estado de origen del Exhorto
    estadoOrigenNombre: str | None = None

    # municipioOrigenNombre: Nombre del municipio de origen del Juzgado/Área que envió el Exhorto
    municipioOrigenNombre: str | None = None

    # fechaHoraRecepcion: Fecha hora local en el que el Poder Judicial exhortado marca que se recibió el Exhorto.
    fechaHoraRecepcion: datetime | None = None

    # municipioTurnadoId: Identificador del municipio que corresponde al Juzgado/Área al que se turnó el Exhorto
    municipioTurnadoId: int | None = None

    # municipioTurnadoNombre: Nombre del municipio del Juzgado/Área al que se turnó el Exhorto
    municipioTurnadoNombre: str | None = None

    # areaTurnadoId: Identificador propio del Poder Judicial Exhortado que corresponde al Juzgado/Área al que se turna el
    # Exhorto y hará el correspondiente proceso de este.
    areaTurnadoId: str | None = None

    # areaTurnadoNombre: Nombre del Juzgado/Área al Exhorto y hará el correspondiente proceso de este.
    areaTurnadoNombre: str | None = None

    # numeroExhorto: Número de Exhorto con el que se radica en el Juzgado/Área que se turnó el exhorto.
    # Este número sirve para que el usuario pueda indentificar su exhorto dentro del Juzgado/Área donde se turnó.
    numeroExhorto: str | None = None

    # urlInfo: Contiene una URL para abrir una página con la información referente a la recepción del exhorto que se realizó.
    # Esta página el Juzgado que envió el exhorto la puede imprimir como acuse de recibido y evidencia de que el exhorto fue
    # enviado correctamente al Poder Judicial exhortado o también una página que muestre el estatus del exhorto.
    urlInfo: str | None = None


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

    # Identificador del Exhorto. Este dato es el identificador con el que el Poder Judicial exhortante identifica su exhorto,
    # y el Poder Judicial exhortado recibe en en endpoint "Recibir Exhorto" en "exhortoOrigenId",
    # ya que el exhorto se responde sobre el identificador del origen. Obligatorio y string.
    exhortoId: str | None = None

    # Identificador propio del Poder Judicial exhortado con el que identifica la respuesta del exhorto.
    # Este dato puede ser un número consecutivo (ej "1", "2", "3"...), un GUID/UUID o
    # cualquíer otro valor con que se identifique la respuesta. Obligatorio y string.
    respuestaOrigenId: str | None = None

    # Identificador del municipio que corresponde al Juzgado/Área al que se turnó el Exhorto y que realiza la respuesta de este.
    # Obligatorio y entero.
    municipioTurnadoId: int | None = None

    # Identificador propio del Poder Judicial exhortado que corresponde al Juzgado/Área
    # al que se turna el Exhorto y está respondiendo. Opcional y string.
    areaTurnadoId: str | None = None

    # Nombre del Juzgado/Área al que el Exhorto se turnó y está respondiendo. Obligatorio y string.
    areaTurnadoNombre: str | None = None

    # Número de Exhorto con el que se radicó en el Juzgado/Área que se turnó el exhorto.
    # Este número sirve para que el usuario pueda indentificar su exhorto dentro del Juzgado/Área donde se turnó.
    # Opcional y string.
    numeroExhorto: str | None = None

    # Valor que representa si se realizó la diligenciación del Exhorto:
    # 0 = No Diligenciado
    # 1 = Parcialmente Dilgenciado
    # 2 = Diligenciado
    # Obligatorio y entero.
    tipoDiligenciado: int | None = None

    # Texto simple referenta a alguna observación u observaciones correspondientes a la respuesta del Exhorto.
    # Opcional y string.
    observaciones: str | None = None

    # Array/Colección de objetos de tipo ArchivoARecibir que corresponden a
    # los archivos de los documentos de la respuesta del Exhorto. Obligatorio
    archivos: list[ExhExhortoArchivoIn] | None = None

    # Array/Colección de objetos de tipo VideoAcceso que representan los accesos a
    # los videos de las audiencias que forman parte de la respuesta. Opcional
    videos: list[ExhExhortoVideoIn] | None = None


class ExhExhortoRecibirRespuestaOut(BaseModel):
    """Respuesta de la operacion Recibir Respuesta Exhorto"""

    # Identificador del Exhorto. Este dato es el identificador con el que el Poder Judicial exhortante identifica su exhorto,
    # y el Poder Judicial exhortado recibe en en endpoint "Recibir Exhorto" en "exhortoOrigenId",
    # ya que el exhorto se responde sobre el identificador del origen. Obligatorio y string.
    exhortoId: str | None = None

    # Identificador propio del Poder Judicial exhortado con el que identifica la respuesta del exhorto.
    # Este dato puede ser un número consecutivo (ej "1", "2", "3"...),
    # un GUID/UUID o cualquíer otro valor con que se identifique la respuesta. Obligatorio y string.
    respuestaOrigenId: str | None = None

    # Fecha hora local del Poder Judicial que recibe la respuesta del Exhorto. Obligatorio y datetime.
    fechaHora: datetime | None = None


class OneExhExhortoRecibirRespuestaOut(OneBaseOut):
    """Esquema para entregar la respuesta de la operacion Recibir Respuesta Exhorto"""

    data: ExhExhortoRecibirRespuestaOut | None = None
