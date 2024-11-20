"""
Exh Exhortos Promociones Archivos v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from carina.core.permisos.models import Permiso
from carina.v4.exh_exhortos_promociones_archivos.crud import get_exh_exhorto_promocion_archivo
from carina.v4.exh_exhortos_promociones_archivos.schemas import ExhExhortoPromocionArchivoOut, OneExhExhortoPromocionArchivoOut
from carina.v4.usuarios.authentications import UsuarioInDB, get_current_active_user
from lib.database import Session, get_db
from lib.exceptions import MyAnyError

exh_exhortos_promociones_archivos = APIRouter(prefix="/v4/exh_exhortos_promociones_archivos", tags=["exh exhortos promociones"])


@exh_exhortos_promociones_archivos.get("/{exh_exhorto_promocion_archivo_id}", response_model=OneExhExhortoPromocionArchivoOut)
def detalle_exh_exhorto_promocion_archivo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_promocion_archivo_id: int,
):
    """Detalle de un archivo de una promoción a partir de su id"""
    if current_user.permissions.get("EXH EXHORTOS PROMOCIONES ARCHIVOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto_promocion_archivo = get_exh_exhorto_promocion_archivo(database, exh_exhorto_promocion_archivo_id)
        data = ExhExhortoPromocionArchivoOut.model_validate(exh_exhorto_promocion_archivo)
    except MyAnyError as error:
        return OneExhExhortoPromocionArchivoOut(success=False, errors=[str(error)])
    return OneExhExhortoPromocionArchivoOut(success=True, data=data)
