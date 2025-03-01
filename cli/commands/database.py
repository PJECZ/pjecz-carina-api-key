"""
Database para comandos de la CLI

Se deben cargar TODOS los modelos para que SQLAlchemy pueda trabajar con la base de datos sin problemas.
"""

from sqlalchemy.orm import Session, sessionmaker

from pjecz_carina_api_key.dependencies.database import get_engine
from pjecz_carina_api_key.models.autoridades import Autoridad
from pjecz_carina_api_key.models.bitacoras import Bitacora
from pjecz_carina_api_key.models.distritos import Distrito
from pjecz_carina_api_key.models.domicilios import Domicilio
from pjecz_carina_api_key.models.entradas_salidas import EntradaSalida
from pjecz_carina_api_key.models.estados import Estado
from pjecz_carina_api_key.models.exh_areas import ExhArea
from pjecz_carina_api_key.models.exh_exhortos import ExhExhorto
from pjecz_carina_api_key.models.exh_exhortos_actualizaciones import ExhExhortoActualizacion
from pjecz_carina_api_key.models.exh_exhortos_archivos import ExhExhortoArchivo
from pjecz_carina_api_key.models.exh_exhortos_partes import ExhExhortoParte
from pjecz_carina_api_key.models.exh_exhortos_promociones import ExhExhortoPromocion
from pjecz_carina_api_key.models.exh_exhortos_promociones_archivos import ExhExhortoPromocionArchivo
from pjecz_carina_api_key.models.exh_exhortos_promociones_promoventes import ExhExhortoPromocionPromovente
from pjecz_carina_api_key.models.exh_exhortos_respuestas_videos import ExhExhortoVideo
from pjecz_carina_api_key.models.exh_externos import ExhExterno
from pjecz_carina_api_key.models.materias import Materia
from pjecz_carina_api_key.models.modulos import Modulo
from pjecz_carina_api_key.models.municipios import Municipio
from pjecz_carina_api_key.models.oficinas import Oficina
from pjecz_carina_api_key.models.permisos import Permiso
from pjecz_carina_api_key.models.roles import Rol
from pjecz_carina_api_key.models.tareas import Tarea
from pjecz_carina_api_key.models.usuarios import Usuario
from pjecz_carina_api_key.models.usuarios_roles import UsuarioRol
from pjecz_carina_api_key.settings import get_settings


def get_session() -> Session:
    """Obtener conexión a la base de datos"""
    engine = get_engine(get_settings())
    return Session(autocommit=False, autoflush=False, bind=engine)
