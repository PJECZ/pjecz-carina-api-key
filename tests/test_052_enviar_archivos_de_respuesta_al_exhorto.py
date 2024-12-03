"""
Unit test - 052 Enviar los Archivos de la Respuesta al Exhorto

Se envían los documentos que conforman la respuesta del exhorto.

- DEBE CONFIGURAR en las variables de entorno FOLIO_SEGUIMIENTO
- Se envía exhortoOrigenId, respuestaOrigenId y el archivo
- POST /exh_exhortos_archivos/responder_upload
- Se recibe el esquema OneExhExhortoArchivoRecibirRespuestaExhortoDataOut.

"""

import time
import unittest

import requests

from tests.load_env import config


class Test052EnviarArchivosDeRespuestaAlExhorto(unittest.TestCase):
    """Test 05b Enviar Archivos de Respuesta al Exhorto"""

    def test_05b_post_exh_exhorto_archivos_respuesta(self):
        """Probar el POST para enviar archivos de respuesta al exhorto"""

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

        # Validar el data
        self.assertEqual(type(contenido["data"]), dict)
        data = contenido["data"]

        # Validar parte del contenido de data
        self.assertEqual("exhortoOrigenId" in data, True)
        self.assertEqual("respuestaOrigenId" in data, True)
        self.assertEqual("archivos" in data, True)

        # Validar que archivos sea una lista
        self.assertEqual(type(data["archivos"]), list)
        archivos = data["archivos"]

        # Bucle para mandar los archivo por multipart/form-data
        for archivo in archivos:
            time.sleep(2)  # Pausa de 2 segundos

            # Validar cada archivo
            self.assertEqual("nombreArchivo" in archivo, True)
            self.assertEqual("hashSha1" in archivo, True)
            self.assertEqual("hashSha256" in archivo, True)
            self.assertEqual("tipoDocumento" in archivo, True)

            # Tomar el nombre del archivo
            archivo_nombre = archivo["nombreArchivo"]

            # Parámetros para el envío del archivo
            params = {
                "exhortoOrigenId": config["exhorto_origen_id"],
                "respuestaOrigenId": data["respuestaOrigenId"],
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
