"""
Unit test - Consultar Estados
"""

import unittest

import requests

from tests import config


class TestsConsultarEstados(unittest.TestCase):
    """Test Consultar Estados"""

    def test_get_estados(self):
        """GET method for estados"""

        # Consultar los estados
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/estados",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("errors" in contenido, True)
        self.assertEqual("data" in contenido, True)

        # Validar que se haya tenido éxito
        if contenido["success"] is False:
            print(f"Errors: {str(contenido['errors'])}")
        self.assertEqual(contenido["success"], True)

        # Validar que se listen los estados
        self.assertEqual(type(contenido["data"]), list)
        for item in contenido["data"]:
            self.assertEqual("clave" in item, True)
            self.assertEqual("nombre" in item, True)

    def test_get_estado_clave(self):
        """GET method for estado with clave"""

        # Consultar el estado definido en la variable de entorno ESTADO_CLAVE
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/estados/{config['estado_clave']}",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("errors" in contenido, True)
        self.assertEqual("data" in contenido, True)

        # Validar que se haya tenido éxito
        if contenido["success"] is False:
            print(f"Errors: {str(contenido['errors'])}")
        self.assertEqual(contenido["success"], True)

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
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("errors" in contenido, True)
        self.assertEqual("data" in contenido, True)

        # Validar que se haya tenido éxito
        if contenido["success"] is False:
            print(f"Errors: {str(contenido['errors'])}")
        self.assertEqual(contenido["success"], True)

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
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("errors" in contenido, True)
        self.assertEqual("data" in contenido, True)

        # Validar que se haya tenido éxito
        if contenido["success"] is False:
            print(f"Errors: {str(contenido['errors'])}")
        self.assertEqual(contenido["success"], True)

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
