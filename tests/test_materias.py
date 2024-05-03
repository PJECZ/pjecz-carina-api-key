"""
Unit test for materias category
"""

import unittest
import requests
from tests.load_env import config


class TestMaterias(unittest.TestCase):
    """Tests for materias category"""

    def test_get_materias(self):
        """Test GET method for materias"""
        response = requests.get(
            f"{config['api_base_url']}/materias",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_materia_clave_fam(self):
        """Test GET method for materia by clave FAM"""
        response = requests.get(
            f"{config['api_base_url']}/materias/FAM",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        self.assertEqual(data["data"]["clave"], "FAM")


if __name__ == "__main__":
    unittest.main()
