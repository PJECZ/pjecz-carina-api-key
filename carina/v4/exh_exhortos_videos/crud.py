"""
Exh Exhorto Videos v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.exh_exhortos_videos.models import ExhExhortoVideo
from ..exh_exhortos.crud import get_exh_exhorto_by_exhorto_origen_id


def get_exh_exhortos_videos(database: Session, exh_exhorto_id: str = None) -> Any:
    """Consultar los videos activos"""
    consulta = database.query(ExhExhortoVideo)
    if exh_exhorto_id is not None:
        exh_exhorto = get_exh_exhorto_by_exhorto_origen_id(database, exh_exhorto_id)
        consulta = consulta.filter_by(exh_exhorto_id=exh_exhorto.id)
    return consulta.filter_by(estatus="A").order_by(ExhExhortoVideo.id)


def get_exh_exhorto_video(database: Session, exh_exhorto_video_id: int) -> ExhExhortoVideo:
    """Consultar un video por su id"""
    exh_exhorto_video = database.query(ExhExhortoVideo).get(exh_exhorto_video_id)
    if exh_exhorto_video is None:
        raise MyNotExistsError("No existe ese video")
    if exh_exhorto_video.estatus != "A":
        raise MyIsDeletedError("No es activo ese video, está eliminado")
    return exh_exhorto_video
