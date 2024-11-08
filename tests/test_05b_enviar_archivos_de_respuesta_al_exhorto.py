"""
Unit test - 05b Enviar los Archivos de la Respuesta al Exhorto
"""

import unittest

import requests

from tests.database import ExhExhorto, get_database_session
from tests.load_env import config


class Test05bEnviarArchivosDeRespuestaAlExhorto(unittest.TestCase):
    """Test 05b Enviar Archivos de Respuesta al Exhorto"""

    def test_05b_post_exh_exhorto_archivos_respuesta(self):
        """Probar el metodo POST para enviar archivos de respuesta al exhorto"""

        # Cargar la sesion de la base de datos para recuperar los datos
        session = get_database_session()

        # Consultar el último exhorto
        exh_exhorto = session.query(ExhExhorto).order_by(ExhExhorto.id.desc()).first()
        if exh_exhorto is None:
            self.fail("No se encontró el último exhorto en database.sqlite")

            # Bucle para mandar los archivo por multipart/form-data
