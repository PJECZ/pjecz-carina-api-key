"""
Bitacoras, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Bitacora(Base, UniversalMixin):
    """Bitacora"""

    # Nombre de la tabla
    __tablename__ = "bitacoras"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    modulo_id = Column(Integer, ForeignKey("modulos.id"), index=True, nullable=False)
    modulo = relationship("Modulo", back_populates="bitacoras")
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=False)
    usuario = relationship("Usuario", back_populates="bitacoras")

    # Columnas
    descripcion = Column(String(256), nullable=False)
    url = Column(String(512), nullable=False)

    def __repr__(self):
        """Representación"""
        return f"<Bitacora {self.creado} {self.descripcion}>"
