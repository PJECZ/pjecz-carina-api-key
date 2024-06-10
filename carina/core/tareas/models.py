"""
Tareas, modelos
"""

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Tarea(Base, UniversalMixin):
    """Tarea"""

    # Nombre de la tabla
    __tablename__ = "tareas"

    # Clave primaria NOTA: El id es string y es el mismo que usa el RQ worker
    id: Mapped[str] = mapped_column(Uuid, primary_key=True)

    # Clave foránea
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="tareas")

    # Columnas
    archivo: Mapped[str] = mapped_column(String(256))
    comando: Mapped[str] = mapped_column(String(256), index=True)
    ha_terminado: Mapped[bool] = mapped_column(default=False)
    mensaje: Mapped[str] = mapped_column(String(1024))
    url: Mapped[str] = mapped_column(String(512))

    def __repr__(self):
        """Representación"""
        return f"<Tarea {self.id}>"
