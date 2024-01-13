"""
Unit tests for autoridades category
"""
import unittest

import requests

from tests.load_env import config


class TestAutoridades(unittest.TestCase):
    """Tests for autoridades category"""

    def test_get_autoridades(self):
        """Test GET method for autoridades"""
        response = requests.get(
            f"{config['api_base_url']}/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_autoridades_by_es_extinto(self):
        """Test GET method for autoridades by es_extinto"""
        response = requests.get(
            f"{config['api_base_url']}/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            params={"es_extinto": 1},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["es_extinto"], 1)


if __name__ == "__main__":
    unittest.main()
