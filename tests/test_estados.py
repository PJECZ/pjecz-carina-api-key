"""
Unit test for estados category
"""

import unittest

import requests

from tests.load_env import config


class TestEstados(unittest.TestCase):
    """Tests for estados category"""

    def test_get_estados(self):
        """Test GET method for estados"""
        response = requests.get(
            url=f"{config['api_base_url']}/estados",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_estado_by_clave_inegi(self):
        """Test GET method for estado by clave INEGI"""
        response = requests.get(
            url=f"{config['api_base_url']}/estados/05",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        self.assertEqual(data["data"]["nombre"], "COAHUILA DE ZARAGOZA")


if __name__ == "__main__":
    unittest.main()
