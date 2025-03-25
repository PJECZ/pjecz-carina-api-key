"""
Autoridades
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.autoridades import Autoridad
from ..models.distritos import Distrito
from ..models.materias import Materia
from ..models.permisos import Permiso
from ..schemas.autoridades import AutoridadOut, OneAutoridadOut
from ..settings import Settings, get_settings

autoridades = APIRouter(prefix="/api/v5/autoridades")


def get_autoridad_with_clave_nd(database: Annotated[Session, Depends(get_db)]) -> Autoridad:
    """Consultar la autoridad con clave ND"""
    try:
        return database.query(Autoridad).filter_by(clave="ND").one()
    except (MultipleResultsFound, NoResultFound) as error:
        raise MyNotExistsError("No existe la autoridad con clave ND") from error


@autoridades.get("/{clave}", response_model=OneAutoridadOut)
async def detalle_autoridad(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una autoridad a partir de su clave"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        autoridad = database.query(Autoridad).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound) as error:
        return OneAutoridadOut(success=False, message="No existe esa autoridad", errors=[str(error)])
    if autoridad.estatus != "A":
        message = "No está habilitada esa autoridad"
        return OneAutoridadOut(success=False, message=message, errors=[message])
    return OneAutoridadOut(success=True, message=f"Detalle de {clave}", data=AutoridadOut.model_validate(autoridad))


@autoridades.get("", response_model=CustomList[AutoridadOut])
async def paginado_autoridades(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    distrito_clave: str = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    materia_clave: str = None,
):
    """Paginado de autoridades"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Autoridad)
    if distrito_clave is not None:
        try:
            distrito_clave = safe_clave(distrito_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave del distrito")
        consulta = consulta.join(Distrito).filter(Distrito.clave == distrito_clave).filter(Distrito.estatus == "A")
    if es_jurisdiccional is not None:
        consulta = consulta.filter(Autoridad.es_jurisdiccional == es_jurisdiccional)
    if es_notaria is not None:
        consulta = consulta.filter(Autoridad.es_notaria == es_notaria)
    if materia_clave is not None:
        try:
            materia_clave = safe_clave(materia_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave de la materia")
        consulta = consulta.join(Materia).filter(Materia.clave == materia_clave).filter(Materia.estatus == "A")
    return paginate(consulta.filter(Autoridad.estatus == "A").order_by(Autoridad.clave))
