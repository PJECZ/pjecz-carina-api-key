"""
Exh Exhortos Videos v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session
from ..dependencies.exceptions import MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_not_implemented import NotImplement
from ..models.exh_exhortos_videos import ExhExhortoVideo
from ..models.permisos import Permiso
from .exh_exhortos import get_exh_exhorto

exh_exhortos_videos = APIRouter(prefix="/v4/exh_exhortos_videos", tags=["exh exhortos"])


def get_exh_exhortos_videos(database: Session, exh_exhorto_id: int) -> Any:
    """Consultar los videos de un exhorto"""
    exh_exhorto = get_exh_exhorto(database, exh_exhorto_id)
    return (
        database.query(ExhExhortoVideo)
        .filter_by(exh_exhorto_id=exh_exhorto.id)
        .filter_by(estatus="A")
        .order_by(ExhExhortoVideo.id)
    )


def get_exh_exhorto_video(database: Session, exh_exhorto_video_id: int) -> ExhExhortoVideo:
    """Consultar un video por su id"""
    exh_exhorto_video = database.query(ExhExhortoVideo).get(exh_exhorto_video_id)
    if exh_exhorto_video is None:
        raise MyNotExistsError("No existe ese video")
    if exh_exhorto_video.estatus != "A":
        raise MyIsDeletedError("No es activo ese video, está eliminado")
    return exh_exhorto_video


@exh_exhortos_videos.get("", response_model=NotImplement)
async def no_implementado(current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)]):
    """Entregar la estructura donde dice que esta ruta no está implementada"""
    if current_user.permissions.get("EXH EXHORTOS VIDEOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return NotImplement(
        success=False,
        message="Esta ruta no está implementada",
        errors=["Not implemented"],
        data=None,
    )
