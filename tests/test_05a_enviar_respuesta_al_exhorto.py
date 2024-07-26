"""
Unit test - 05a Enviar Respuesta al Exhorto
"""

import random
import string
import unittest
from datetime import datetime

import lorem
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

        # Elegir aleatoriamente un municipio del estado de Coahuila de Zaragoza (clave 05)
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/municipios/05",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)
        contenido = response.json()
        municipio = random.choice(contenido["data"])

        # Elegir aleatoriamente el area a donde se va a turnar el exhorto
        exh_area_clave = random.choice(["SLT-OCP", "TRC-OCP"])
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/exh_areas/{exh_area_clave}",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)
        contenido = response.json()
        exh_area = contenido["data"]

        # Definir aleatoriamente un número de exhorto
        numero = random.randint(1, 9999)
        numero_exhorto = f"{numero}/{datetime.now().year}"

        # Definir aleatoriamente el tipo de diligenciado
        tipo_diligenciado = random.choice(["", "OFICIO", "PETICION DE PARTE"])

        # Definir aleatoriamente las observaciones
        observaciones = lorem.sentence()

        # Definir aleatoriamente definir los archivos de la respuesta
        archivos = []
        for numero in range(1, random.randint(1, 2) + 1):
            archivos.append(
                {
                    "nombreArchivo": f"prueba-{numero}.pdf",
                    "hashSha1": "3a9a09bbb22a6da576b2868c4b861cae6b096050",
                    "hashSha256": "df3d983d24a5002e7dcbff1629e25f45bb3def406682642643efc4c1c8950a77",
                    "tipoDocumento": 1,
                }
            )

        # Definir aleatoriamente definir los videos de la respuesta
        videos = []
        for numero in range(1, random.randint(1, 2) + 1):
            characters = string.ascii_letters + string.digits
            random_video_id = "".join(random.choice(characters) for _ in range(11))
            videos.append(
                {
                    "titulo": f"Video {numero}",
                    "descripcion": lorem.sentence(),
                    "fecha": datetime.now().isoformat(),
                    "urlAcceso": f"https://www.youtube.com/watch?v={random_video_id}",
                }
            )

        # Definir los datos que se van a mandar
        datos = {
            "exhortoId": exh_exhorto.exhorto_origen_id,
            "respuestaOrigenId": respuesta_origen_id,
            "municipioTurnadoId": municipio["clave"],
            "areaTurnadoId": exh_area["clave"],
            "areaTurnadoNombre": exh_area["nombre"],
            "numeroExhorto": numero_exhorto,
            "tipoDiligenciado": tipo_diligenciado,
            "observaciones": observaciones,
            "archivos": archivos,
            "videos": videos,
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

        # Validar el data
        self.assertEqual(type(contenido["data"]), dict)
        data = contenido["data"]

        # Validar el contenido de data
        self.assertEqual("exhortoId" in data, True)
        self.assertEqual("respuestaOrigenId" in data, True)
        self.assertEqual("fechaHora" in data, True)

        # Guardar respuestaOrigenId en la base de datos
        exh_exhorto.exhorto_id = data["exhortoId"]
        exh_exhorto.respuesta_origen_id = data["respuestaOrigenId"]
        session.commit()


if __name__ == "__main__":
    unittest.main()
