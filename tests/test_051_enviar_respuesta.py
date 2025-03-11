"""
Unit test - Enviar Respuesta
"""

import random
import string
import unittest
from datetime import datetime

import lorem
import requests
from sqlalchemy.sql import or_

from pjecz_carina_api_key.dependencies.pwgen import generar_identificador
from tests import config
from tests.database import TestExhExhorto, TestExhExhortoRespuesta, TestExhExhortoRespuestaArchivo, get_database_session


class TestsEnviarRespuesta(unittest.TestCase):
    """Tests Enviar Respuesta"""

    def test_post_respuesta(self):
        """Probar el POST para enviar una respuesta al exhorto"""

        # Cargar la sesión de la base de datos para recuperar los datos de la prueba anterior
        session = get_database_session()

        # Consultar el último exhorto RECIBIDO CON EXITO, TRANSFERIDO, PROCESANDO
        test_exh_exhorto = (
            session.query(TestExhExhorto)
            .filter(
                or_(
                    TestExhExhorto.estado == "RECIBIDO",
                    TestExhExhorto.estado == "RECIBIDO CON EXITO",
                    TestExhExhorto.estado == "TRANSFERIDO",
                    TestExhExhorto.estado == "PROCESANDO",
                )
            )
            .order_by(TestExhExhorto.id.desc())
            .first()
        )
        if test_exh_exhorto is None:
            self.fail("No se encontró un exhorto RECIBIDO, RECIBIDO CON EXITO, TRANSFERIDO o PROCESANDO en sqlite")

        # Generar el identificador propio del PJ exhortado con el que identifica la respuesta del exhorto
        respuesta_origen_id = generar_identificador()

        # Consultar y elegir aleatoriamente un municipio del PJ que responde
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/municipios/{test_exh_exhorto.estado_origen_id}",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)
        contenido = response.json()
        municipio = random.choice(contenido["data"])

        # Elaborar una clave del área al azar del PJ que responde
        area_numero = random.randint(1, 99)
        area_turnado_id = f"A{area_numero}"

        # Elaborar un nombre del área al azar del PJ que responde
        area_turnado_nombre = f"AREA HIPOTETICA NO. {area_numero}"

        # Elaborar aleatoriamente un número de exhorto
        numero = random.randint(1, 9999)
        numero_exhorto = f"{numero}/{datetime.now().year}"

        # Elegir aleatoriamente el tipo de diligenciado
        tipo_diligenciado = random.randint(0, 2)  # 0 = No Diligenciado, 1 = Parcialmente Dilgenciado, 2 = Diligenciado

        # Definir aleatoriamente las observaciones
        observaciones = lorem.sentence()

        # Definir aleatoriamente definir los archivos que se recibirán más adelante
        archivos = []
        for numero in range(1, random.randint(1, 4) + 1):  # Hasta 4 archivos
            archivos.append(
                {
                    "nombreArchivo": f"prueba-{numero}.pdf",
                    "hashSha1": config["archivo_pdf_hashsha1"],
                    "hashSha256": config["archivo_pdf_hashsha256"],
                    "tipoDocumento": 1,
                }
            )

        # Definir aleatoriamente definir los videos
        videos = []
        for numero in range(1, random.randint(1, 2) + 1):  # Hasta 2 videos
            characters = string.ascii_letters + string.digits
            random_video_id = "".join(random.choice(characters) for _ in range(11))
            videos.append(
                {
                    "titulo": f"Video {numero}",
                    "descripcion": lorem.sentence(),
                    "fecha": datetime.now().strftime("%Y-%m-%d"),
                    "urlAcceso": f"https://www.youtube.com/watch?v={random_video_id}",
                }
            )

        # Definir los datos de la respuesta del exhorto
        payload_for_json = {
            "exhortoId": test_exh_exhorto.exhorto_origen_id,
            "respuestaOrigenId": respuesta_origen_id,
            "municipioTurnadoId": int(municipio["clave"]),
            "areaTurnadoId": area_turnado_id,
            "areaTurnadoNombre": area_turnado_nombre,
            "numeroExhorto": numero_exhorto,
            "tipoDiligenciado": tipo_diligenciado,
            "observaciones": observaciones,
            "archivos": archivos,
            "videos": videos,
        }

        # Mandar la respuesta
        try:
            respuesta = requests.post(
                url=f"{config['api_base_url']}/exh_exhortos/recibir_respuesta",
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
        self.assertEqual("respuestaOrigenId" in data, True)
        self.assertEqual("fechaHora" in data, True)

        # Insertar la respuesta en SQLite
        test_exh_exhorto_respuesta = TestExhExhortoRespuesta(
            test_exh_exhorto=test_exh_exhorto,
            test_exh_exhorto_id=test_exh_exhorto.id,
            respuesta_origen_id=data["respuestaOrigenId"],
            estado="PENDIENTE",
        )
        session.add(test_exh_exhorto_respuesta)
        session.commit()

        # Insertar los archivos de la respuesta del exhorto en SQLite
        for archivo in archivos:
            test_exh_exhorto_respuesta_archivo = TestExhExhortoRespuestaArchivo(
                test_exh_exhorto_respuesta=test_exh_exhorto_respuesta,
                test_exh_exhorto_respuesta_id=test_exh_exhorto_respuesta.id,
                nombre_archivo=archivo["nombreArchivo"],
                hash_sha1=archivo["hashSha1"],
                hash_sha256=archivo["hashSha256"],
                tipo_documento=archivo["tipoDocumento"],
            )
            session.add(test_exh_exhorto_respuesta_archivo)
            session.commit()

        # Cerrar la sesión SQLite
        session.close()


if __name__ == "__main__":
    unittest.main()
