"""
Unit test - 05a Enviar Respuesta al Exhorto
"""

import random
import unittest
from datetime import datetime

import requests
from requests.exceptions import ConnectionError

from lib.pwgen import generar_identificador
from tests.database import ExhExhorto, get_database_session
from tests.load_env import config


class Test05aEnviarRespuestaAlExhorto(unittest.TestCase):
    """Test 05a Enviar Respuesta al Exhorto"""

    def test_05a_post_exh_exhorto_respuesta(self):
        """Probar el metodo POST para enviar una respuesta al exhorto"""

        # Cargar la sesion de la base de datos para recuperar los datos
        session = get_database_session()

        # Consultar el último exhorto
        exh_exhorto = session.query(ExhExhorto).order_by(ExhExhorto.id.desc()).first()
        if exh_exhorto is None:
            self.fail("No se encontró el último exhorto en database.sqlite")

        # Generar el respuesta_origen_id como el identidicador de la respuesta del exhorto del PJ exhortante
        respuesta_origen_id = generar_identificador()

        # TODO: Elegir aleatoriamente el municipio

        # TODO: Elegir aleatoriamente el area a donde se va a turnar el exhorto

        # TODO: Definir un numero de exhorto

        # TODO: Elegir aleatoriamente el tipo de diligenciado

        # TODO: Definir las observaciones

        # TODO: Aleatoriamente definir los archivos de la respuesta

        # TODO: Aleatoriamente definir los videos de la respuesta

        # Definir los datos que se van a mandar
        datos = {
            "exhortoId": exh_exhorto.exhorto_origen_id,
            "respuestaOrigenId": respuesta_origen_id,
            "municipioTurnadoId": "",
            "areaTurnadoId": "",
            "areaTurnadoNombre": "",
            "numeroExhorto": "",
            "tipoDiligenciado": "",
            "observaciones": "",
            "archivos": "",
            "videos": "",
        }

        # Mandar la respuesta del exhorto
        try:
            respuesta = requests.post(
                url=f"{config['api_base_url']}/exh_exhortos/responder",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
                json=datos,
            )
        except ConnectionError as error:
            self.fail(error)
        self.assertEqual(respuesta.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = respuesta.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("errors" in contenido, True)
        self.assertEqual("data" in contenido, True)


if __name__ == "__main__":
    unittest.main()
