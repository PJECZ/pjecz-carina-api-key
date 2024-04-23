"""
Estados, modelos
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Estado(Base, UniversalMixin):
    """Estado"""

    # Nombre de la tabla
    __tablename__ = "estados"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    clave = Column(String(3), nullable=False)
    nombre = Column(String(256), nullable=False)

    # Hijos
    municipios = relationship("Municipio", back_populates="estado")

    def __repr__(self):
        """Representación"""
        return f"<Estado {self.id}>"
