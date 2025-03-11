"""
Unit test - Enviar Promoción
"""

import random
import string
import unittest
from datetime import datetime

import lorem
import requests
from faker import Faker
from sqlalchemy.sql import or_

from tests import config
from tests.database import TestExhExhorto, TestExhExhortoPromocion, TestExhExhortoPromocionArchivo, get_database_session


class TestsEnviarPromocion(unittest.TestCase):
    """Tests Enviar Promoción"""

    def test_post_promocion(self):
        """Probar el POST para enviar una promoción"""

        # Cargar la sesión de la base de datos para recuperar los datos de la prueba anterior
        session = get_database_session()

        # Consultar el último exhorto RESPONDIDO o CONTESTADO
        test_exh_exhorto = (
            session.query(TestExhExhorto)
            .filter(or_(TestExhExhorto.estado == "RESPONDIDO", TestExhExhorto.estado == "CONTESTADO"))
            .order_by(TestExhExhorto.id.desc())
            .first()
        )
        if test_exh_exhorto is None:
            self.fail("No se encontró un exhorto RESPONDIDO o CONTESTADO en sqlite")

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
        for numero in range(1, random.randint(1, 4) + 1):  # Hasta 4 archivos
            archivo = {
                "nombreArchivo": f"prueba-{numero}.pdf",
                "hashSha1": config["archivo_pdf_hashsha1"],
                "hashSha256": config["archivo_pdf_hashsha256"],
                "tipoDocumento": random.randint(1, 3),
            }
            archivos.append(archivo)

        # Generar un folio de origen de la promoción
        characters = string.ascii_letters + string.digits
        folio_origen_promocion = "".join(random.choice(characters) for _ in range(11))

        # Definir los datos de la promoción
        payload_for_json = {
            "folioSeguimiento": test_exh_exhorto.folio_seguimiento,
            "folioOrigenPromocion": folio_origen_promocion,
            "promoventes": promoventes,
            "fojas": random.randint(2, 9),
            "fechaOrigen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "observaciones": lorem.sentence(),
            "archivos": archivos,
        }

        # Mandar la promoción
        try:
            respuesta = requests.post(
                url=f"{config['api_base_url']}/recibir_promocion",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
                json=payload_for_json,
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

        # Validar que se haya tenido éxito
        if contenido["success"] is False:
            print(f"Errors: {str(contenido['errors'])}")
        self.assertEqual(contenido["success"], True)

        # Validar el data
        self.assertEqual(type(contenido["data"]), dict)
        data = contenido["data"]

        # Validar el contenido de data
        self.assertEqual("folioOrigenPromocion" in data, True)
        self.assertEqual("folioSeguimiento" in data, True)
        self.assertEqual("fechaHora" in data, True)

        # Validar que nos regrese el mismo folio_origen_promocion
        self.assertEqual(data["folioOrigenPromocion"], folio_origen_promocion)

        # Cargar la sesión de SQLite para conservar los datos para las pruebas siguientes
        session = get_database_session()

        # Insertar la promoción en SQLite
        test_exh_exhorto_promocion = TestExhExhortoPromocion(
            test_exh_exhorto=test_exh_exhorto,
            test_exh_exhorto_id=test_exh_exhorto.id,
            folio_origen_promocion=folio_origen_promocion,
            folio_seguimiento=data["folioSeguimiento"],
            estado="PENDIENTE",
        )
        session.add(test_exh_exhorto_promocion)
        session.commit()

        # Insertar los archivos de la promoción en SQLite
        for archivo in archivos:
            exh_exhorto_promocion_archivo = TestExhExhortoPromocionArchivo(
                test_exh_exhorto_promocion=test_exh_exhorto_promocion,
                test_exh_exhorto_promocion_id=test_exh_exhorto_promocion.id,
                nombre_archivo=archivo["nombreArchivo"],
                hash_sha1=archivo["hashSha1"],
                hash_sha256=archivo["hashSha256"],
                tipo_documento=archivo["tipoDocumento"],
            )
            session.add(exh_exhorto_promocion_archivo)
            session.commit()

        # Cerrar la sesión SQLite
        session.close()


if __name__ == "__main__":
    unittest.main()
