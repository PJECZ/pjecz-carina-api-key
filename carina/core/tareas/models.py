"""
Tareas, modelos
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Tarea(Base, UniversalMixin):
    """Tarea"""

    # Nombre de la tabla
    __tablename__ = "tareas"

    # Clave primaria NOTA: El id es string y es el mismo que usa el RQ worker
    id = Column(String(36), primary_key=True)

    # Clave foránea
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=False)
    usuario = relationship("Usuario", back_populates="tareas")

    # Columnas
    comando = Column(String(256), nullable=False, index=True)
    mensaje = Column(String(1024), default="", server_default="")
    ha_terminado = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        """Representación"""
        return f"<Tarea {self.id}>"
