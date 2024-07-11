"""
Unit test for municipios category
"""

import unittest

import requests

from tests.load_env import config


class TestMunicipios(unittest.TestCase):
    """Tests for municipios category"""

    def test_get_municipios(self):
        """Test GET method for municipios"""
        response = requests.get(
            url=f"{config['api_base_url']}/municipios",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_municipio_by_clave_inegi(self):
        """Test GET method for municipio by clave INEGI"""
        response = requests.get(
            url=f"{config['api_base_url']}/municipios/66",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        self.assertEqual(data["data"]["nombre"], "SALTILLO")


if __name__ == "__main__":
    unittest.main()
