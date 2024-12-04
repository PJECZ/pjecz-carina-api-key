"""
Unit test - Enviar Promoción

Se pueden enviar o recibir promociones sobre exhortos radicados.

"""

import unittest

import requests

from tests.load_env import config


class TestsEnviarPromocion(unittest.TestCase):
    """Tests Enviar Promoción"""

    def test_post_promocion(self):
        """Probar el POST para enviar una promoción"""


if __name__ == "__main__":
    unittest.main()
