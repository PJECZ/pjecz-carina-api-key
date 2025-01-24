"""
Autoridades, modelos
"""

from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class Autoridad(Base, UniversalMixin):
    """Autoridad"""

    # Nombre de la tabla
    __tablename__ = "autoridades"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Claves foráneas
    distrito_id: Mapped[int] = mapped_column(ForeignKey("distritos.id"))
    distrito: Mapped["Distrito"] = relationship(back_populates="autoridades")
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.id"))
    materia: Mapped["Materia"] = relationship(back_populates="autoridades")
    municipio_id: Mapped[int] = mapped_column(ForeignKey("municipios.id"))
    municipio: Mapped["Municipio"] = relationship(back_populates="autoridades")

    # Columnas
    clave: Mapped[str] = mapped_column(String(16), unique=True)
    descripcion: Mapped[str] = mapped_column(String(256))
    descripcion_corta: Mapped[str] = mapped_column(String(64))
    es_extinto: Mapped[bool] = mapped_column(default=False)

    # Hijos
    exh_exhortos: Mapped[List["ExhExhorto"]] = relationship("ExhExhorto", back_populates="autoridad")
    usuarios: Mapped[List["Usuario"]] = relationship("Usuario", back_populates="autoridad")

    def __repr__(self):
        """Representación"""
        return f"<Autoridad {self.clave}>"
