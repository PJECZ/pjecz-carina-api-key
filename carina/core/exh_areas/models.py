"""
Exh Areas, modelos
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class ExhArea(Base, UniversalMixin):
    """ExhArea"""

    # Nombre de la tabla
    __tablename__ = "exh_areas"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    clave = Column(String(16), unique=True, nullable=False)
    descripcion = Column(String(256), nullable=False)

    # Hijos
    exh_exhortos = relationship("ExhExhorto", back_populates="exh_area")

    def __repr__(self):
        """Representación"""
        return f"<ExhArea {self.clave}>"
