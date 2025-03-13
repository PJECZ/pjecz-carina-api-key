"""
Unit test - Enviar Actualización
"""

import random
import string
import unittest
from datetime import datetime

import lorem
import requests

from tests import config
from tests.database import TestExhExhorto, get_database_session


class TestsEnviarActualizacion(unittest.TestCase):
    """Tests Enviar Actualización"""

    def test_post_actualizacion(self):
        """Probar el POST para enviar una actualización"""

        # Cargar la sesión de la base de datos para recuperar los datos de la prueba anterior
        session = get_database_session()

        # Consultar el último exhorto
        test_exh_exhorto = session.query(TestExhExhorto).order_by(TestExhExhorto.id.desc()).first()
        if test_exh_exhorto is None:
            self.fail("No se encontró un exhorto en sqlite")

        # Generar un identificador de actualización de origen de 10 caracteres al azar
        characters = string.ascii_letters + string.digits
        actualizacion_origen_id = "".join(random.choice(characters) for _ in range(11))

        # Definir los datos de la actualización
        payload_for_json = {
            "exhortoId": test_exh_exhorto.exhorto_origen_id,
            "actualizacionOrigenId": actualizacion_origen_id,
            "tipoActualizacion": random.choice(["AreaTurnado", "NumeroExhorto"]),
            "fechaHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "descripcion": lorem.sentence(),
        }

        # Mandar la actualización
        try:
            respuesta = requests.post(
                url=f"{config['api_base_url']}/exh_exhortos/actualizar",
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
        self.assertEqual("exhortoId" in data, True)
        self.assertEqual("actualizacionOrigenId" in data, True)
        self.assertEqual("fechaHora" in data, True)

        # Validar que nos regrese el mismo exhorto_origen_id
        self.assertEqual(data["exhortoId"], test_exh_exhorto.exhorto_origen_id)

        # Cerrar la sesión sqlite
        session.close()


if __name__ == "__main__":
    unittest.main()
