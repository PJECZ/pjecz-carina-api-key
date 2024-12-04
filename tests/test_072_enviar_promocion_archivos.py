"""
Unit test - Enviar Archivos de la Promoción

Se pueden enviar o recibir promociones sobre exhortos radicados.

"""

import unittest

import requests

from tests.load_env import config


class TestsEnviarArchivosPromocion(unittest.TestCase):
    """Tests Enviar Archivos de la Promoción"""

    def test_post_archivos_promocion(self):
        """Probar el POST para enviar archivos de una promoción"""


if __name__ == "__main__":
    unittest.main()
