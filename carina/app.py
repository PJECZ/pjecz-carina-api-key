"""
PJECZ Carina API Key
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from carina.v4.autoridades.paths import autoridades
from carina.v4.bitacoras.paths import bitacoras
from carina.v4.distritos.paths import distritos
from carina.v4.domicilios.paths import domicilios
from carina.v4.entradas_salidas.paths import entradas_salidas
from carina.v4.estados.paths import estados
from carina.v4.exh_areas.paths import exh_areas
from carina.v4.exh_exhortos.paths import exh_exhortos
from carina.v4.exh_exhortos_actualizaciones.paths import exh_exhortos_actualizaciones
from carina.v4.exh_exhortos_archivos.paths import exh_exhortos_archivos
from carina.v4.exh_exhortos_partes.paths import exh_exhortos_partes
from carina.v4.exh_exhortos_promociones.paths import exh_exhortos_promociones
from carina.v4.exh_exhortos_promociones_archivos.paths import exh_exhortos_promociones_archivos
from carina.v4.exh_exhortos_promociones_promoventes.paths import exh_exhortos_promociones_promoventes
from carina.v4.exh_exhortos_videos.paths import exh_exhortos_videos
from carina.v4.exh_externos.paths import exh_externos
from carina.v4.materias.paths import materias
from carina.v4.modulos.paths import modulos
from carina.v4.municipios.paths import municipios
from carina.v4.oficinas.paths import oficinas
from carina.v4.permisos.paths import permisos
from carina.v4.roles.paths import roles
from carina.v4.tareas.paths import tareas
from carina.v4.usuarios.paths import usuarios
from carina.v4.usuarios_roles.paths import usuarios_roles
from config.settings import get_settings
from lib.fastapi_validation_exception_handler import validation_exception_handler


def create_app() -> FastAPI:
    """Crea la aplicación FastAPI"""

    # FastAPI
    app = FastAPI(
        title="PJECZ Carina API Key",
        description="API con autentificación para enviar y recibir exhortos.",
        docs_url="/docs",
        redoc_url=None,
    )

    # CORSMiddleware
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins.split(","),
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    # Override the default validation exception handler
    app.add_exception_handler(RequestValidationError, handler=validation_exception_handler)

    # Rutas
    app.include_router(autoridades, include_in_schema=False)
    app.include_router(bitacoras, include_in_schema=False)
    app.include_router(distritos, include_in_schema=False)
    app.include_router(domicilios, include_in_schema=False)
    app.include_router(entradas_salidas, include_in_schema=False)
    app.include_router(estados, include_in_schema=False)
    app.include_router(exh_areas)
    app.include_router(exh_exhortos)
    app.include_router(exh_exhortos_actualizaciones)
    app.include_router(exh_exhortos_archivos)
    app.include_router(exh_exhortos_partes)
    app.include_router(exh_exhortos_promociones)
    app.include_router(exh_exhortos_promociones_archivos)
    app.include_router(exh_exhortos_promociones_promoventes)
    app.include_router(exh_exhortos_videos)
    app.include_router(exh_externos)
    app.include_router(materias)
    app.include_router(modulos, include_in_schema=False)
    app.include_router(municipios, include_in_schema=False)
    app.include_router(oficinas, include_in_schema=False)
    app.include_router(permisos, include_in_schema=False)
    app.include_router(roles, include_in_schema=False)
    app.include_router(tareas, include_in_schema=False)
    app.include_router(usuarios, include_in_schema=False)
    app.include_router(usuarios_roles, include_in_schema=False)

    # Paginación
    add_pagination(app)

    # Mensaje de Bienvenida
    @app.get("/")
    async def root():
        """Mensaje de Bienvenida"""
        return {"message": "API con autentificación para enviar y recibir exhortos."}

    # Entregar
    return app
