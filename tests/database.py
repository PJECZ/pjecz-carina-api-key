"""
Database for tests

Para conservar los datos de la respuesta en test_02_enviar_exhorto y
pasarlos a las siguientes pruebas, se usa una base de datos SQLite.
"""

from pathlib import Path
from typing import List, Optional

from sqlalchemy import Engine, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, Session, mapped_column, relationship, sessionmaker


class Base(DeclarativeBase, MappedAsDataclass):
    """Base class for declarative base"""

    pass


class ExhExhorto(Base):
    """ExhExhorto"""

    __tablename__ = "exh_exhortos"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    exhorto_origen_id: Mapped[str]
    folio_seguimiento: Mapped[Optional[str]]

    exh_exhortos_archivos: Mapped[List["ExhExhortoArchivo"]] = relationship(
        "ExhExhortoArchivo",
        back_populates="exh_exhorto",
        init=False,
    )


class ExhExhortoArchivo(Base):
    """ExhExhortoArchivo"""

    __tablename__ = "exh_exhortos_archivos"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    exh_exhorto_id: Mapped[int] = mapped_column(ForeignKey("exh_exhortos.id"))
    exh_exhorto: Mapped["ExhExhorto"] = relationship(back_populates="exh_exhortos_archivos")

    nombre_archivo: Mapped[str]
    hash_sha1: Mapped[str]
    hash_sha256: Mapped[str]
    tipo_documento: Mapped[int]


def get_engine() -> Engine:
    """Database engine"""

    # File for database
    database_file = Path("tests/database.sqlite")

    # Create engine
    engine = create_engine(f"sqlite:///{database_file}")

    # Create tables if tests.sqlite does not exist
    if not database_file.exists():
        with engine.begin() as connection:
            Base.metadata.create_all(connection)

    return engine


def get_database_session() -> Session:
    """Database session"""

    # Create engine
    engine = get_engine()

    # Create session
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create database session
    database = session_local()

    return database
