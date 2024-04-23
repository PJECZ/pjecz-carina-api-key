"""
Exhortos, modelos
"""

from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Exhorto(Base, UniversalMixin):
    """Exhorto"""

    # Nombre de la tabla
    __tablename__ = "exhortos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # UUID identificador con el que el PJ exhortante identifica el exhorto que envía
    exhorto_origen_id = Column(String(64), nullable=False, unique=True)

    # Identificador INEGI del Municipio del Estado del PJ exhortado al que se quiere enviar el Exhorto
    municipio_destino_id = Column(Integer, ForeignKey("municipios.id"), index=True, nullable=False)
    municipio_destino = relationship("Municipio", back_populates="exhortos_destinos")

    # Clave de la materia (el que se obtuvo en la consulta de materias del PJ exhortado) al que el Exhorto hace referencia
    materia_id = Column(Integer, ForeignKey("materias.id"), index=True, nullable=False)
    materia = relationship("Materia", back_populates="exhortos")

    # Identificador INEGI del Estado de origen del Municipio donde se ubica el Juzgado del PJ exhortante
    # estado_origen_id = Column(Integer, ForeignKey("estados.id"), index=True, nullable=False)
    # estado_origen = relationship("Estado", back_populates="exhortos")

    # Identificador INEGI del Municipio donde está localizado el Juzgado del PJ exhortante
    municipio_origen_id = Column(Integer, ForeignKey("municipios.id"), index=True, nullable=False)
    municipio_origen = relationship("Municipio", back_populates="exhortos_origenes")

    # Identificador propio del Juzgado/Área que envía el Exhorto
    juzgado_origen_id = Column(String(64))

    # Nombre del Juzgado/Área que envía el Exhorto
    juzgado_origen_nombre = Column(String(256), nullable=False)

    # El número de expediente (o carpeta procesal, carpeta...) que tiene el asunto en el Juzgado de Origen
    # numeroExpedienteOrigen    string SI
    numero_expediente_origen = Column(String(256), nullable=False)

    # numeroOficioOrigen        string NO
    # tipoJuicioAsuntoDelitos   string SI
    # juezExhortante            string NO
    # partes                    PersonaParte[] NO
    # fojas                     int SI
    # diasResponder             int SI
    # tipoDiligenciacionNombre  string NO
    # fechaOrigen               datetime NO
    # observaciones             string NO
    # archivos                  ArchivoARecibir[] SI

    @property
    def estadoOrigenId(self):
        """ID del estado de origen"""
        return self.municipio_origen.estado_id

    @property
    def materiaClave(self):
        """Clave de la materia"""
        return self.materia.clave

    @property
    def municipioOrigenId(self):
        """ID del municipio de origen"""
        return self.municipio_origen_id

    def __repr__(self):
        """Representación"""
        return f"<Exhorto {self.id}>"
