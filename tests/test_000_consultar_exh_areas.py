"""
Unit test - Consultar ExhAreas
"""

import unittest

import requests

from tests import config


class TestsConsultarExhAreas(unittest.TestCase):
    """Tests Consultar ExhAreas"""

    def test_get_exh_areas(self):
        """GET method for exh_areas"""

        # Consultar las exh_areas
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/exh_areas",
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

        # Validar que se listen las exh_areas
        self.assertEqual(type(contenido["data"]), list)
        for item in contenido["data"]:
            self.assertEqual("clave" in item, True)
            self.assertEqual("nombre" in item, True)

    def test_get_exh_area_clave_nd(self):
        """GET method for exh_area by clave ND"""

        # Consultar el area ND
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/exh_areas/ND",
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

        # Validar que sea la clave ND y el nombre NO DEFINIDO
        self.assertEqual(data["clave"], "ND")
        self.assertEqual(data["nombre"], "NO DEFINIDO")

    def test_get_exh_area_clave_slt_ocp(self):
        """GET method for exh_area by clave SLT-OCP"""

        # Consultar el area SLT-OCP
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/exh_areas/SLT-OCP",
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

        # Validar que sea la clave SLT-OCP y el nombre SOLICITUD DE OCUPACION
        self.assertEqual(data["clave"], "SLT-OCP")
        self.assertEqual(data["nombre"], "OFICIALIA COMUN DE PARTES DE SALTILLO")

    def test_get_exh_area_clave_trc_ocp(self):
        """GET method for exh_area by clave TRC-OCP"""

        # Consultar el area TRC-OCP
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/exh_areas/TRC-OCP",
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

        # Validar que sea la clave TRC-OCP y el nombre TRAMITE DE OCUPACION
        self.assertEqual(data["clave"], "TRC-OCP")
        self.assertEqual(data["nombre"], "OFICIALIA COMUN DE PARTES DE TORREON")


if __name__ == "__main__":
    unittest.main()
