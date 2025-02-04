"""
PJECZ Carina API Key
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from .dependencies.fastapi_validation_exception_handler import validation_exception_handler
from .routers.autoridades import autoridades
from .routers.bitacoras import bitacoras
from .routers.distritos import distritos
from .routers.domicilios import domicilios
from .routers.entradas_salidas import entradas_salidas
from .routers.estados import estados
from .routers.exh_areas import exh_areas
from .routers.exh_exhortos import exh_exhortos
from .routers.exh_exhortos_actualizaciones import exh_exhortos_actualizaciones
from .routers.exh_exhortos_archivos import exh_exhortos_archivos
from .routers.exh_exhortos_partes import exh_exhortos_partes
from .routers.exh_exhortos_promociones import exh_exhortos_promociones
from .routers.exh_exhortos_promociones_archivos import exh_exhortos_promociones_archivos
from .routers.exh_exhortos_promociones_promoventes import exh_exhortos_promociones_promoventes
from .routers.exh_exhortos_videos import exh_exhortos_videos
from .routers.exh_externos import exh_externos
from .routers.materias import materias
from .routers.modulos import modulos
from .routers.municipios import municipios
from .routers.oficinas import oficinas
from .routers.permisos import permisos
from .routers.roles import roles
from .routers.tareas import tareas
from .routers.usuarios import usuarios
from .routers.usuarios_roles import usuarios_roles
from .settings import get_settings

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
app.include_router(estados)
app.include_router(exh_areas, include_in_schema=False)
app.include_router(exh_exhortos)
app.include_router(exh_exhortos_actualizaciones)
app.include_router(exh_exhortos_archivos)
app.include_router(exh_exhortos_partes, include_in_schema=False)
app.include_router(exh_exhortos_promociones)
app.include_router(exh_exhortos_promociones_archivos)
app.include_router(exh_exhortos_promociones_promoventes, include_in_schema=False)
app.include_router(exh_exhortos_videos, include_in_schema=False)
app.include_router(exh_externos, include_in_schema=False)
app.include_router(materias, include_in_schema=False)
app.include_router(modulos, include_in_schema=False)
app.include_router(municipios)
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
