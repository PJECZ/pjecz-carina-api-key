"""
Unit test - 05b Enviar Archivos de Respuesta al Exhorto
"""

import unittest

import requests
from requests.exceptions import ConnectionError

from tests.database import ExhExhorto, get_database_session
from tests.load_env import config


class Test05bEnviarArchivosDeRespuestaAlExhorto(unittest.TestCase):
    """Test 05b Enviar Archivos de Respuesta al Exhorto"""

    def test_05b_post_exh_exhorto_archivos_respuesta(self):
        """Probar el metodo POST para enviar archivos de respuesta al exhorto"""

        pass
