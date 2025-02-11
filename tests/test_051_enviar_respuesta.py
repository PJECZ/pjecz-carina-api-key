"""
Unit test - Enviar Respuesta

Se envían los datos que conforman la respuesta del exhorto.

- DEBE CONFIGURAR en las variables de entorno FOLIO_SEGUIMIENTO
- Se manda el esquema ExhExhortoRecibirRespuestaIn que contiene archivos (ExhExhortoArchivoIn) y videos (ExhExhortoVideoIn).
- POST /exh_exhortos/responder
- Se recibe el esquema OneExhExhortoRecibirRespuestaOut.

"""

import random
import string
import time
import unittest
from datetime import datetime

import lorem
import requests

from tests import config
from tests.database import ExhExhorto, ExhExhortoArchivo, get_database_session


def generar_identificador(largo: int = 16) -> str:
    """Generar identificador con el tiempo actual y algo aleatorio, todo con letras en mayúsculas y dígitos"""
    timestamp_unique = str(int(time.time() * 1000))
    random_characters = "".join(random.sample(string.ascii_uppercase + string.digits, k=largo))
    return f"{timestamp_unique}{random_characters}"[:largo]


class TestsEnviarRespuesta(unittest.TestCase):
    """Tests Enviar Respuesta"""

    def test_post_respuesta(self):
        """Probar el POST para enviar una respuesta al exhorto"""

        # Validar que se haya configurado la variable de entorno FOLIO_SEGUIMIENTO
        if config["folio_seguimiento"] == "":
            self.fail("No se ha configurado la variable de entorno FOLIO_SEGUIMIENTO")

        # Consultar el exhorto
        try:
            respuesta = requests.get(
                url=f"{config['api_base_url']}/exh_exhortos/{config['folio_seguimiento']}",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(respuesta.status_code, 200)

        # Validar el contenido
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

        # Validar el contenido QUE NOS INTERESA de data
        self.assertEqual("exhortoOrigenId" in data, True)
        self.assertEqual("folioSeguimiento" in data, True)
        self.assertEqual("estadoDestinoId" in data, True)
        self.assertEqual("estadoDestinoNombre" in data, True)
        self.assertEqual("municipioDestinoId" in data, True)
        self.assertEqual("municipioDestinoNombre" in data, True)

        # Generar el identificador propio del PJ exhortado con el que identifica la respuesta del exhorto
        respuesta_origen_id = generar_identificador()

        # Elegir aleatoriamente un municipio del PJ que responde
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/municipios/{data['estadoDestinoId']}",
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
        datos = {
            "exhortoId": data["exhortoOrigenId"],
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

        # Cargar la sesión de SQLite para conservar los datos para las pruebas siguientes
        session = get_database_session()

        # Consultar el último exhorto
        exh_exhorto = session.query(ExhExhorto).order_by(ExhExhorto.id.desc()).first()
        if exh_exhorto is None:
            self.fail("No se encontró el último exhorto en database.sqlite")

        # Actualizar en el exhorto la respuesta_origen_id
        exh_exhorto.respuesta_origen_id = data["exhortoOrigenId"]
        session.add(exh_exhorto)
        session.commit()

        # Insertar los archivos de la respuesta del exhorto en SQLite
        for archivo in archivos:
            exh_exhorto_archivo = ExhExhortoArchivo(
                exh_exhorto=exh_exhorto,
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
