"""
Exh Exhortos Archivos, modelos
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class ExhExhortoArchivo(Base, UniversalMixin):
    """ExhExhortoArchivo"""

    # Nombre de la tabla
    __tablename__ = "exh_exhortos_archivos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    exh_exhorto_id = Column(Integer, ForeignKey("exh_exhortos.id"), index=True, nullable=False)
    exh_exhorto = relationship("ExhExhorto", back_populates="exh_exhortos_archivos")

    # Nombre del archivo, como se enviará. Este debe incluir el la extensión del archivo.
    nombre_archivo = Column(String(256), nullable=False)

    # Hash SHA1 en hexadecimal que corresponde al archivo a recibir. Esto para comprobar la integridad del archivo.
    hash_sha1 = Column(String(256))

    # Hash SHA256 en hexadecimal que corresponde al archivo a recibir. Esto apra comprobar la integridad del archivo.
    hash_sha256 = Column(String(256))

    # Identificador del tipo de documento que representa el archivo:
    # 1 = Oficio
    # 2 = Acuerdo
    # 3 = Anexo
    tipo_documento = Column(Integer, nullable=False)

    # URL del archivo en Google Storage
    url = Column(String(512), nullable=False, default="", server_default="")

    @property
    def nombreArchivo(self):
        """Nombre del archivo"""
        return self.nombre_archivo

    @property
    def hashSha1(self):
        """Hash SHA1"""
        return self.hash_sha1

    @property
    def hashSha256(self):
        """Hash SHA256"""
        return self.hash_sha256

    @property
    def tipoDocumento(self):
        """Tipo de documento"""
        return self.tipo_documento

    def __repr__(self):
        """Representación"""
        return f"<ExhExhortoArchivo {self.id}>"
