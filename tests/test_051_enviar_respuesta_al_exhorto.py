"""
Unit test - 051 Enviar la Respuesta al Exhorto

Se envían los datos que conforman la respuesta del exhorto.

Se manda el esquema ExhExhortoRecibirRespuestaIn que contiene archivos (ExhExhortoArchivoIn) y videos (ExhExhortoVideoIn).

- POST /exh_exhortos/responder

Se recibe el esquema OneExhExhortoRecibirRespuestaOut.

"""

import random
import string
import unittest
from datetime import datetime

import lorem
import requests

from lib.pwgen import generar_identificador
from tests.database import ExhExhorto, ExhExhortoArchivo, get_database_session
from tests.load_env import config


class Test051EnviarRespuestaAlExhorto(unittest.TestCase):
    """Test 05a Enviar Respuesta al Exhorto"""

    def test_05a_post_exh_exhorto_respuesta(self):
        """Probar el POST para enviar una respuesta al exhorto"""

        # Cargar la sesión de la base de datos para recuperar los datos
        session = get_database_session()

        # Consultar el último exhorto
        exh_exhorto = session.query(ExhExhorto).order_by(ExhExhorto.id.desc()).first()
        if exh_exhorto is None:
            self.fail("No se encontró el último exhorto en database.sqlite")

        # Validar que el estado de origen sea 05 (Coahuila de Zaragoza)

        # Generar el identificador de la respuesta del exhorto del PJ exhortante
        exhorto_id = generar_identificador()

        # Elegir aleatoriamente un municipio del PJ que responde

        # Elaborar una clave del área al azar del PJ que responde

        # Elaborar un nombre del área al azar del PJ que responde

        # Elaborar aleatoriamente un número de exhorto
        numero = random.randint(1, 9999)
        numero_exhorto = f"{numero}/{datetime.now().year}"

        # Elegir aleatoriamente el tipo de diligenciado
        tipo_diligenciado = random.choice(["", "OFICIO", "PETICION DE PARTE"])

        # Definir aleatoriamente las observaciones
        observaciones = lorem.sentence()

        # Definir aleatoriamente definir los archivos que se recibirán más adelante
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

        # Definir aleatoriamente definir los videos
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

        # Definir los datos de la respuesta del exhorto
        datos = {
            "exhortoId": None,  # string
            "respuestaOrigenId": None,  # string
            "municipioTurnadoId": None,  # int
            "areaTurnadoId": None,  # string
            "areaTurnadoNombre": None,  # string
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
        self.assertEqual("exhortoId" in data, True)
        self.assertEqual("respuestaOrigenId" in data, True)
        self.assertEqual("fechaHora" in data, True)

        # Actualizar el registro del exhorto en la base de datos SQLite
        exh_exhorto.respuesta_origen_id = data["respuestaOrigenId"]
        session.commit()

        # Insertar los registros de los archivos en la base de datos SQLite
        for archivo in archivos:
            exh_exhorto_archivo = ExhExhortoArchivo(
                exh_exhorto_id=exh_exhorto.id,
                nombre_archivo=archivo["nombreArchivo"],
                hash_sha1=archivo["hashSha1"],
                hash_sha256=archivo["hashSha256"],
                tipo_documento=archivo["tipoDocumento"],
                es_respuesta=True,
            )
            session.add(exh_exhorto_archivo)
            session.commit()


if __name__ == "__main__":
    unittest.main()
