"""
Unit test - Consultar Municipios
"""

import unittest

import requests

from tests.load_env import config


class TestsConsultarMunicipios(unittest.TestCase):
    """Tests Consultar Municipios"""

    def test_get_municipios_estado_clave_05(self):
        """GET method for municipios for estado with clave 05"""

        # Consultar los municipios
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/municipios/05",
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

        # Validar que se listen los municipios
        self.assertEqual(type(contenido["data"]), list)
        for item in contenido["data"]:
            self.assertEqual("clave" in item, True)
            self.assertEqual("nombre" in item, True)

    def test_get_estado_clave_05_municipio_clave_30(self):
        """GET method for estado with clave 05 and municipio with clave 30"""

        # Consultar el municipio
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/municipios/05/30",
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

        # Validar el data
        self.assertEqual(type(contenido["data"]), dict)
        data = contenido["data"]
        self.assertEqual("clave" in data, True)
        self.assertEqual("nombre" in data, True)

        # Validar que el estado sea Coahuila de Zaragoza y el municipio sea Saltillo
        self.assertEqual(data["clave"], "030")
        self.assertEqual(data["nombre"], "SALTILLO")
        self.assertEqual(data["estado_clave"], "05")
        self.assertEqual(data["estado_nombre"], "COAHUILA DE ZARAGOZA")


if __name__ == "__main__":
    unittest.main()
