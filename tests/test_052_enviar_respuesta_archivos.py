"""
Unit test - Enviar los Archivos de la Respuesta

Se envían los documentos que conforman la respuesta del exhorto.

- DEBE CONFIGURAR en las variables de entorno FOLIO_SEGUIMIENTO
- Se envía exhortoOrigenId, respuestaOrigenId y el archivo
- POST /exh_exhortos_archivos/responder_upload
- Se recibe el esquema OneExhExhortoArchivoRecibirRespuestaExhortoDataOut.

"""

import time
import unittest
from pathlib import Path

import requests

from tests import config
from tests.database import ExhExhorto, ExhExhortoArchivo, get_database_session


class TestsEnviarRespuestaArchivos(unittest.TestCase):
    """Tests Enviar Respuesta Archivos"""

    def test_post_respuesta_archivos(self):
        """Probar el POST para enviar archivos de respuesta al exhorto"""

        # Validar que se haya configurado la variable de entorno FOLIO_SEGUIMIENTO
        if config["folio_seguimiento"] == "":
            self.fail("No se ha configurado la variable de entorno FOLIO_SEGUIMIENTO")

        # Cargar la sesión de la base de datos para recuperar los datos de la prueba anterior
        session = get_database_session()

        # Consultar el último exhorto
        exh_exhorto = session.query(ExhExhorto).order_by(ExhExhorto.id.desc()).first()
        if exh_exhorto is None:
            self.fail("No se encontró el último exhorto en database.sqlite")

        # Parámetros para el envío del archivo
        params = {
            "exhortoOrigenId": exh_exhorto.exhorto_origen_id,
            "respuestaOrigenId": exh_exhorto.respuesta_origen_id,
        }

        # Bucle para mandar los archivo por multipart/form-data
        data_acuse = None
        for archivo in exh_exhorto.exh_exhortos_archivos:
            # Si es_respuesta es Falso, se omite
            if archivo.es_respuesta is False:
                continue

            # Pausa de 2 segundos
            print(f"{archivo.nombre_archivo}...")
            time.sleep(2)

            # Tomar el nombre del archivo
            archivo_nombre = archivo.nombre_archivo

            # Validar que el archivo exista
            respuesta_archivo = Path(f"tests/{archivo_nombre}")
            if not respuesta_archivo.exists():
                self.fail(f"El archivo {archivo_nombre} no existe")

            # Leer el archivo de prueba
            with open(respuesta_archivo, "rb") as archivo_prueba:
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

                # Validar que se haya tenido éxito
                if contenido["success"] is False:
                    print(f"Errors: {str(contenido['errors'])}")
                self.assertEqual(contenido["success"], True)

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

        # Validar que data_acuse NO sea nulo
        self.assertEqual(data_acuse is not None, True)

        # Validar el último acuse
        self.assertEqual(type(data_acuse), dict)
        self.assertEqual("exhortoId" in data_acuse, True)
        self.assertEqual("respuestaOrigenId" in data_acuse, True)
        self.assertEqual("fechaHoraRecepcion" in data_acuse, True)


if __name__ == "__main__":
    unittest.main()
