"""
Unit test - Consultar Materias

Listado de materias del PJ exhortado.

- GET /materias
- GET /materias/{MATERIA_CLAVE}

"""

import unittest

import requests

from tests import config


class TestsConsultarMaterias(unittest.TestCase):
    """Tests Consultar Materias"""

    def test_get_materias(self):
        """GET method for materias"""

        # Consultar las materias
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/materias",
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

        # Validar que se listen las materias
        self.assertEqual(type(contenido["data"]), list)
        for item in contenido["data"]:
            self.assertEqual("clave" in item, True)
            self.assertEqual("nombre" in item, True)
            self.assertEqual("descripcion" in item, True)

    def test_get_materia_clave_civ(self):
        """GET method for materia by clave CIV"""

        # Consultar la materia civil
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/materias/CIV",
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
        self.assertEqual("descripcion" in data, True)

        # Validar la materia civil
        self.assertEqual(data["clave"], "CIV")
        self.assertEqual(data["nombre"], "CIVIL")


if __name__ == "__main__":
    unittest.main()
