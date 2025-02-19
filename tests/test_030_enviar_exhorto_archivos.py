"""
Unit test - Enviar los Archivos del Exhorto

Se manda exhortoOrigenId y el archivo

- POST /exh_exhortos_archivos/upload

Se recibe el esquema OneExhExhortoArchivoFileOut.
"""

import time
import unittest
from pathlib import Path

import requests

from tests import config
from tests.database import ExhExhorto, get_database_session


class TestsEnviarExhortosArchivos(unittest.TestCase):
    """Tests Enviar Exhorto Archivos"""

    def test_post_exhorto_archivos(self):
        """Probar el POST para enviar los archivos de un exhorto"""

        # Cargar la sesión de la base de datos para recuperar los datos de la prueba anterior
        session = get_database_session()

        # Consultar el último exhorto
        exh_exhorto = session.query(ExhExhorto).order_by(ExhExhorto.id.desc()).first()
        if exh_exhorto is None:
            self.fail("No se encontró el último exhorto en database.sqlite")

        # Definir los datos que se van a incluir en el envío de los archivos
        payload_for_data = {"exhortoOrigenId": exh_exhorto.exhorto_origen_id}

        # Bucle para mandar los archivo por multipart/form-data
        for exh_exhorto_archivo in exh_exhorto.exh_exhortos_archivos:
            time.sleep(2)  # Pausa de 2 segundos

            # Tomar el nombre del archivo
            archivo_nombre = exh_exhorto_archivo.nombre_archivo

            # Validar que el archivo exista
            archivo_ruta = Path(f"tests/{archivo_nombre}")
            if not archivo_ruta.is_file():
                self.fail(f"No se encontró el archivo {archivo_nombre}")

            # Leer el archivo de prueba
            with open(f"tests/{archivo_nombre}", "rb") as archivo_prueba:
                # Mandar el archivo
                try:
                    respuesta = requests.post(
                        url=f"{config['api_base_url']}/exh_exhortos_archivos/upload",
                        headers={"X-Api-Key": config["api_key"]},
                        timeout=config["timeout"],
                        files={"archivo": (archivo_nombre, archivo_prueba, "application/pdf")},
                        data=payload_for_data,
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
                self.assertEqual("archivo" in data, True)
                data_archivo = data["archivo"]
                self.assertEqual("acuse" in data, True)
                data_acuse = data["acuse"]

                # Validar que dentro de archivo venga nombreArchivo y tamaño
                self.assertEqual(type(data_archivo), dict)
                self.assertEqual("nombreArchivo" in data_archivo, True)
                self.assertEqual("tamaño" in data_archivo, True)

        # Validar el último acuse
        self.assertEqual(type(data_acuse), dict)
        self.assertEqual("exhortoOrigenId" in data_acuse, True)
        self.assertEqual("folioSeguimiento" in data_acuse, True)
        self.assertEqual("fechaHoraRecepcion" in data_acuse, True)
        self.assertEqual("municipioAreaRecibeId" in data_acuse, True)
        self.assertEqual("areaRecibeId" in data_acuse, True)
        self.assertEqual("areaRecibeNombre" in data_acuse, True)
        self.assertEqual("urlInfo" in data_acuse, True)

        # Validar que se recibe el mismo exhortoOrigenId
        self.assertEqual(type(data_acuse["exhortoOrigenId"]), str)
        self.assertEqual(data_acuse["exhortoOrigenId"], exh_exhorto.exhorto_origen_id)

        # Validar que se recibe el folioSeguimiento
        self.assertEqual(type(data_acuse["folioSeguimiento"]), str)
        self.assertNotEqual(data_acuse["folioSeguimiento"], "")

        # Guardar el folio de seguimiento en la base de datos
        exh_exhorto.folio_seguimiento = data_acuse["folioSeguimiento"]
        session.commit()


if __name__ == "__main__":
    unittest.main()
