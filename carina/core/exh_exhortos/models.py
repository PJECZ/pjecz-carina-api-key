"""
Exh Exhortos, modelos
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class ExhExhorto(Base, UniversalMixin):
    """ExhExhorto"""

    # Nombre de la tabla
    __tablename__ = "exh_exhortos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # UUID identificador con el que el PJ exhortante identifica el exhorto que envía
    exhorto_origen_id = Column(String(64), nullable=False, unique=True)

    # Identificador INEGI del Municipio del Estado del PJ exhortado al que se quiere enviar el Exhorto
    municipio_destino_id = Column(Integer, nullable=False)

    # Clave de la materia (el que se obtuvo en la consulta de materias del PJ exhortado) al que el Exhorto hace referencia
    materia_id = Column(Integer, ForeignKey("materias.id"), index=True, nullable=False)
    materia = relationship("Materia", back_populates="exh_exhortos")

    # Identificador INEGI del Estado de origen del Municipio donde se ubica el Juzgado del PJ exhortante
    # estado_origen_id = Column(Integer, ForeignKey("estados.id"), index=True, nullable=False)
    # estado_origen = relationship("Estado", back_populates="exhortos")

    # Identificador INEGI del Municipio donde está localizado el Juzgado del PJ exhortante
    municipio_origen_id = Column(Integer, ForeignKey("municipios.id"), index=True, nullable=False)
    municipio_origen = relationship("Municipio", back_populates="exh_exhortos_origenes")

    # Identificador propio del Juzgado/Área que envía el Exhorto
    juzgado_origen_id = Column(String(64))

    # Nombre del Juzgado/Área que envía el Exhorto
    juzgado_origen_nombre = Column(String(256), nullable=False)

    # El número de expediente (o carpeta procesal, carpeta...) que tiene el asunto en el Juzgado de Origen
    numero_expediente_origen = Column(String(256), nullable=False)

    # El número del oficio con el que se envía el exhorto, el que corresponde al control interno del Juzgado de origen
    numero_oficio_origen = Column(String(256))

    # Nombre del tipo de Juicio, o asunto, listado de los delitos (para materia Penal) que corresponde al Expediente del cual el Juzgado envía el Exhorto
    tipo_juicio_asunto_delitos = Column(String(256), nullable=False)

    # Nombre completo del Juez del Juzgado o titular del Área que envía el Exhorto
    juez_exhortante = Column(String(256))

    # Número de fojas que contiene el exhorto. El valor 0 significa "No Especificado"
    fojas = Column(Integer, nullable=False)

    # Cantidad de dias a partir del día que se recibió en el Poder Judicial exhortado que se tiene para responder el Exhorto. El valor de 0 significa "No Especificado"
    dias_responder = Column(Integer, nullable=False)

    # Nombre del tipo de diligenciación que le corresponde al exhorto enviado. Este puede contener valores como "Oficio", "Petición de Parte"
    tipo_diligenciacion_nombre = Column(String(256))

    # Fecha y hora en que el Poder Judicial exhortante registró que se envió el exhorto en su hora local. En caso de no enviar este dato, el Poder Judicial exhortado puede tomar su fecha hora local.
    fecha_origen = Column(DateTime, server_default=func.now())

    # Texto simple que contenga información extra o relevante sobre el exhorto.
    observaciones = Column(String(1024))

    # Hijos
    # PersonaParte[] NO Contiene la definición de las partes del Expediente
    exh_exhortos_partes = relationship("ExhExhortoParte", back_populates="exh_exhorto")
    # ArchivoARecibir[] SI Colección de los datos referentes a los archivos que se van a recibir el Poder Judicial exhortado en el envío del Exhorto.
    exh_exhortos_archivos = relationship("ExhExhortoArchivo", back_populates="exh_exhorto")

    # Propiedades que se van a cargar despues
    partes = []
    archivos = []

    @property
    def exhortoOrigenId(self):
        """ID del exhorto de origen"""
        return self.exhorto_origen_id

    @property
    def municipioDestinoId(self):
        """Clave INEGI del municipio de destino"""
        return self.municipio_destino_id

    @property
    def materiaClave(self):
        """Clave de la materia"""
        return self.materia.clave

    @property
    def estadoOrigenId(self):
        """Clave INEGI del estado de origen"""
        return self.municipio_origen.estado.clave

    @property
    def municipioOrigenId(self):
        """Clave INEGI del municipio de origen"""
        return self.municipio_origen.clave

    @property
    def juzgadoOrigenId(self):
        """ID del juzgado de origen"""
        return self.juzgado_origen_id

    @property
    def juzgadoOrigenNombre(self):
        """Nombre del juzgado de origen"""
        return self.juzgado_origen_nombre

    @property
    def numeroExpedienteOrigen(self):
        """Número de expediente de origen"""
        return self.numero_expediente_origen

    @property
    def numeroOficioOrigen(self):
        """Número de oficio de origen"""
        return self.numero_oficio_origen

    @property
    def tipoJuicioAsuntoDelitos(self):
        """Tipo de juicio"""
        return self.tipo_juicio_asunto_delitos

    @property
    def juezExhortante(self):
        """Juez exhortante"""
        return self.juez_exhortante

    @property
    def diasResponder(self):
        """Días para responder"""
        return self.dias_responder

    @property
    def tipoDiligenciacionNombre(self):
        """Tipo de diligenciación"""
        return self.tipo_diligenciacion_nombre

    @property
    def fechaOrigen(self):
        """Fecha de origen"""
        return self.fecha_origen

    def __repr__(self):
        """Representación"""
        return f"<ExhExhorto {self.exhorto_origen_id}>"
