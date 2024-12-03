"""
Database para comandos de la CLI

Se deben cargar TODOS los modelos para que SQLAlchemy pueda trabajar con la base de datos sin problemas.
"""

from sqlalchemy.orm import Session, sessionmaker

from carina.core.autoridades.models import Autoridad
from carina.core.bitacoras.models import Bitacora
from carina.core.distritos.models import Distrito
from carina.core.domicilios.models import Domicilio
from carina.core.entradas_salidas.models import EntradaSalida
from carina.core.estados.models import Estado
from carina.core.exh_areas.models import ExhArea
from carina.core.exh_exhortos.models import ExhExhorto
from carina.core.exh_exhortos_actualizaciones.models import ExhExhortoActualizacion
from carina.core.exh_exhortos_archivos.models import ExhExhortoArchivo
from carina.core.exh_exhortos_partes.models import ExhExhortoParte
from carina.core.exh_exhortos_promociones.models import ExhExhortoPromocion
from carina.core.exh_exhortos_promociones_archivos.models import ExhExhortoPromocionArchivo
from carina.core.exh_exhortos_promociones_promoventes.models import ExhExhortoPromocionPromovente
from carina.core.exh_exhortos_videos.models import ExhExhortoVideo
from carina.core.exh_externos.models import ExhExterno
from carina.core.materias.models import Materia
from carina.core.modulos.models import Modulo
from carina.core.municipios.models import Municipio
from carina.core.oficinas.models import Oficina
from carina.core.permisos.models import Permiso
from carina.core.roles.models import Rol
from carina.core.tareas.models import Tarea
from carina.core.usuarios.models import Usuario
from carina.core.usuarios_roles.models import UsuarioRol
from config.settings import get_settings
from lib.database import get_engine


def get_session() -> Session:
    """Obtener conexión a la base de datos"""
    engine = get_engine(get_settings())
    return Session(autocommit=False, autoflush=False, bind=engine)
