"""
Exh Exhortos Videos v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from lib.database import Session, get_db
from lib.exceptions import MyAnyError

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_exh_exhorto_video
from .schemas import OneExhExhortoVideoOut

exh_exhortos_videos = APIRouter(prefix="/v4/exh_exhortos_videos", tags=["exhortos"])


@exh_exhortos_videos.get("/{exh_exhorto_video_id}", response_model=OneExhExhortoVideoOut)
async def detalle_exh_exhorto_video(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_video_id: int,
):
    """Detalle de un video a partir de su id"""
    if current_user.permissions.get("EXH EXHORTOS VIDEOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        exh_exhorto_video = get_exh_exhorto_video(database, exh_exhorto_video_id)
    except MyAnyError as error:
        return OneExhExhortoVideoOut(success=False, errors=[str(error)])
    return OneExhExhortoVideoOut(success=True, data=exh_exhorto_video)
