"""
Unit test - Enviar Actualización

Se puede realizar este proceso cuando el exhorto llega a una Oficialía y se turna a un Juzgado.

Se manda el esquema ExhExhortoActualizarIn.

"""

import unittest

import requests

from tests.load_env import config


class TestsEnviarActualizacion(unittest.TestCase):
    """Tests Enviar Actualización"""

    def test_post_actualizacion(self):
        """Probar el POST para enviar una actualización"""


if __name__ == "__main__":
    unittest.main()
