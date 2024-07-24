"""
Unit test - 00 Consultar Estados
"""

import unittest

import requests
from requests.exceptions import ConnectionError

from tests.load_env import config


class Test00ConsultarEstados(unittest.TestCase):
    """Tests for 01 consultar estados"""

    def test_get_estados(self):
        """GET method for estados"""

        # Consultar los estados
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/estados",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("errors" in contenido, True)
        self.assertEqual("data" in contenido, True)

        # Validar que se listen los estados
        self.assertEqual(type(contenido["data"]), list)
        for item in contenido["data"]:
            self.assertEqual("clave" in item, True)
            self.assertEqual("nombre" in item, True)

    def test_get_estado_clave_05(self):
        """GET method for estado with clave 05 nombre COAHUILA DE ZARAGOZA"""

        # Consultar el estado aguascalientes
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/estados/05",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("errors" in contenido, True)
        self.assertEqual("data" in contenido, True)

        # Validar el data
        self.assertEqual(type(contenido["data"]), dict)
        data = contenido["data"]
        self.assertEqual("clave" in data, True)
        self.assertEqual("nombre" in data, True)

        # Validar que el estado con clave INEGI 05 sea Coahuila de Zaragoza
        self.assertEqual(data["clave"], "05")
        self.assertEqual(data["nombre"], "COAHUILA DE ZARAGOZA")

    def test_get_estado_clave_10(self):
        """GET method for estado with clave 10 nombre DURANGO"""

        # Consultar el estado aguascalientes
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/estados/10",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("errors" in contenido, True)
        self.assertEqual("data" in contenido, True)

        # Validar el data
        self.assertEqual(type(contenido["data"]), dict)
        data = contenido["data"]
        self.assertEqual("clave" in data, True)
        self.assertEqual("nombre" in data, True)

        # Validar que el estado con clave INEGI 10 sea Durango
        self.assertEqual(data["clave"], "10")
        self.assertEqual(data["nombre"], "DURANGO")

    def test_get_estado_clave_19(self):
        """GET method for estado with clave 19 nombre NUEVO LEON"""

        # Consultar el estado aguascalientes
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/estados/19",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("errors" in contenido, True)
        self.assertEqual("data" in contenido, True)

        # Validar el data
        self.assertEqual(type(contenido["data"]), dict)
        data = contenido["data"]
        self.assertEqual("clave" in data, True)
        self.assertEqual("nombre" in data, True)

        # Validar que el estado con clave INEGI 19 sea Nuevo León
        self.assertEqual(data["clave"], "19")
        self.assertEqual(data["nombre"], "NUEVO LEON")


if __name__ == "__main__":
    unittest.main()
