"""
Unit test - 05b Enviar los Archivos de la Respuesta al Exhorto

Se envían los documentos que conforman la respuesta del exhorto.

Se envía exhortoOrigenId, respuestaOrigenId y el archivo

- POST /exh_exhortos_archivos/responder_upload

Se recibe el esquema OneExhExhortoArchivoRecibirRespuestaExhortoDataOut.

"""

import time
import unittest

import requests

from tests.database import ExhExhorto, ExhExhortoArchivo, get_database_session
from tests.load_env import config


class Test05bEnviarArchivosDeRespuestaAlExhorto(unittest.TestCase):
    """Test 05b Enviar Archivos de Respuesta al Exhorto"""

    def test_05b_post_exh_exhorto_archivos_respuesta(self):
        """Probar el POST para enviar archivos de respuesta al exhorto"""

        # Cargar la sesión de SQLite para recuperar los datos
        session = get_database_session()

        # Consultar el último exhorto
        exh_exhorto = session.query(ExhExhorto).order_by(ExhExhorto.id.desc()).first()
        if exh_exhorto is None:
            self.fail("No se encontró el último exhorto en database.sqlite")

        # Consultar en SQLite los archivos que se van a enviar como respuesta
        exh_exhorto_archivos = (
            session.query(ExhExhortoArchivo).filter_by(exh_exhorto_id=exh_exhorto.id).filter_by(es_respuesta=True).all()
        )

        # Bucle para mandar los archivo por multipart/form-data
        for exh_exhorto_archivo in exh_exhorto_archivos:
            time.sleep(2)  # Pausa de 2 segundos

            # Tomar el nombre del archivo
            archivo_nombre = exh_exhorto_archivo.nombre_archivo

            # Parámetros para el envío del archivo
            params = {
                "exhortoOrigenId": exh_exhorto.exhorto_origen_id,
                "respuestaOrigenId": exh_exhorto.respuesta_origen_id,
            }

            # Leer el archivo de prueba
            with open(f"tests/{archivo_nombre}", "rb") as archivo_prueba:
                # Mandar el archivo
                try:
                    respuesta = requests.post(
                        url=f"{config['api_base_url']}/exh_exhortos_archivos/responder_upload",
                        headers={"X-Api-Key": config["api_key"]},
                        timeout=config["timeout"],
                        params=params,
                        files={"archivo": (archivo_nombre, archivo_prueba, "application/pdf")},
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

                # Validar que dentro de data venga archivo
                self.assertEqual("archivo" in data, True)
                data_archivo = data["archivo"]
                self.assertEqual(type(data_archivo), dict)

                # Validar que dentro de archivo venga nombreArchivo y tamaño
                self.assertEqual("nombreArchivo" in data_archivo, True)
                self.assertEqual("tamaño" in data_archivo, True)

                # Validar que dentro de data venga acuse
                self.assertEqual("acuse" in data, True)
                data_acuse = data["acuse"]

        # Validar el último acuse
        self.assertEqual("exhortoId" in data_acuse, True)
        self.assertEqual("respuestaOrigenId" in data_acuse, True)
        self.assertEqual("fechaHoraRecepcion" in data_acuse, True)


if __name__ == "__main__":
    unittest.main()
