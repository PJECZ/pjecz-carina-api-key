"""
Unit test - Enviar Promoción

Se pueden enviar o recibir promociones sobre exhortos radicados.

"""

import random
import string
import unittest
from datetime import datetime

import lorem
import requests
from faker import Faker

from tests.database import ExhExhorto, get_database_session
from tests.load_env import config


class TestsEnviarPromocion(unittest.TestCase):
    """Tests Enviar Promoción"""

    def test_post_promocion(self):
        """Probar el POST para enviar una promoción"""

        # Cargar la sesión de la base de datos para recuperar los datos de la prueba anterior
        session = get_database_session()

        # Consultar el último exhorto
        exh_exhorto = session.query(ExhExhorto).order_by(ExhExhorto.id.desc()).first()
        if exh_exhorto is None:
            self.fail("No se encontró el último exhorto en database.sqlite")

        # Inicializar el generador de nombres aleatorios
        faker = Faker(locale="es_MX")

        # Definir los datos de los promoventes
        promoventes = []
        for _ in range(random.randint(1, 3)):
            genero = faker.random_element(elements=("M", "F"))
            if genero == "F":
                nombre = faker.first_name_female()
            else:
                nombre = faker.first_name_male()
            promoventes.append(
                {
                    "nombre": nombre,
                    "apellidoPaterno": faker.last_name(),
                    "apellidoMaterno": faker.last_name(),
                    "genero": genero,
                    "esPersonaMoral": False,
                    "tipoParte": 0,
                    "tipoParteNombre": "",
                }
            )

        # Definir los datos de los archivos
        archivos = []
        for numero in range(random.randint(1, 3)):
            archivo = {
                "nombreArchivo": f"archivo-{numero}.pdf",
                "hashSha1": "3a9a09bbb22a6da576b2868c4b861cae6b096050",
                "hashSha256": "df3d983d24a5002e7dcbff1629e25f45bb3def406682642643efc4c1c8950a77",
                "tipoDocumento": random.randint(1, 3),
            }
            archivos.append(archivo)

        # Generar un folio de origen de la promoción
        characters = string.ascii_letters + string.digits
        folio_origen_promocion = "".join(random.choice(characters) for _ in range(11))

        # Definir los datos de la promoción
        datos = {
            "folioSeguimiento": exh_exhorto.folio_seguimiento,
            "folioOrigenPromocion": folio_origen_promocion,
            "promoventes": promoventes,
            "fojas": random.randint(2, 9),
            "fechaOrigen": datetime.now(),
            "observaciones": lorem.sentence(),
            "archivos": archivos,
        }

        # Mandar la promoción
        try:
            respuesta = requests.post(
                url=f"{config['api_base_url']}/exh_exhortos_promociones",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
                json=datos,
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(respuesta.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = respuesta.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("errors" in contenido, True)
        self.assertEqual("data" in contenido, True)

        # Validar el data
        self.assertEqual(type(contenido["data"]), dict)
        data = contenido["data"]

        # Validar el contenido de data
        self.assertEqual("folioOrigenPromocion" in data, True)
        self.assertEqual("fechaHora" in data, True)

        # Validar que nos regrese el mismo folio_origen_promocion
        self.assertEqual(data["folioOrigenPromocion"], folio_origen_promocion)


if __name__ == "__main__":
    unittest.main()
