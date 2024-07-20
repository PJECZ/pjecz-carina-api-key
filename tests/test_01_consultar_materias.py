"""
Unit test - 01 Consultar Materias
"""

import unittest

import requests

from tests.load_env import config


class Test01ConsultarMaterias(unittest.TestCase):
    """Tests for 01 consultar materias"""

    def test_01_get_materias(self):
        """Test GET method for materias"""

        # Consultar las materias
        response = requests.get(
            url=f"{config['api_base_url']}/materias",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("errors" in contenido, True)
        self.assertEqual("data" in contenido, True)

        # Validar que se listen las materias
        self.assertEqual(type(contenido["data"]), list)
        for item in contenido["data"]:
            self.assertEqual("clave" in item, True)
            self.assertEqual("nombre" in item, True)
            self.assertEqual("descripcion" in item, True)

    def test_01_get_materia_clave_civ(self):
        """Test GET method for materia by clave CIV"""

        # Consultar la materia civil
        response = requests.get(
            url=f"{config['api_base_url']}/materias/CIV",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
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
        self.assertEqual("descripcion" in data, True)

        # Validar la materia civil
        self.assertEqual(data["clave"], "CIV")
        self.assertEqual(data["nombre"], "CIVIL")

    def test_01_get_materia_clave_fam(self):
        """Test GET method for materia by clave FAM"""

        # Consultar la materia familiar
        response = requests.get(
            url=f"{config['api_base_url']}/materias/FAM",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
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
        self.assertEqual("descripcion" in data, True)

        # Validar la materia familiar
        self.assertEqual(data["clave"], "FAM")
        self.assertEqual(data["nombre"], "FAMILIAR")

    def test_01_get_materia_clave_lab(self):
        """Test GET method for materia by clave LAB"""

        # Consultar la materia laboral
        response = requests.get(
            url=f"{config['api_base_url']}/materias/LAB",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
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
        self.assertEqual("descripcion" in data, True)

        # Validar data materia laboral
        self.assertEqual(data["clave"], "LAB")
        self.assertEqual(data["nombre"], "LABORAL")

    def test_01_get_materia_clave_mer(self):
        """Test GET method for materia by clave MER"""

        # Consultar la materia mercantil
        response = requests.get(
            url=f"{config['api_base_url']}/materias/MER",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
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
        self.assertEqual("descripcion" in data, True)

        # Validar la materia mercantil
        self.assertEqual(data["clave"], "MER")
        self.assertEqual(data["nombre"], "MERCANTIL")


if __name__ == "__main__":
    unittest.main()
