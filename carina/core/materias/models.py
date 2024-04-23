"""
Materias, modelos
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Materia(Base, UniversalMixin):
    """Materia"""

    # Nombre de la tabla
    __tablename__ = "materias"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    clave = Column(String(16), nullable=False, unique=True)
    nombre = Column(String(64), unique=True, nullable=False)
    descripcion = Column(String(1024), nullable=False)

    # Hijos
    exhortos = relationship("Exhorto", back_populates="materia")

    def __repr__(self):
        """Representación"""
        return f"<Materia {self.id}>"
