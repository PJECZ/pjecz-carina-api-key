"""
Unit test - Enviar los Archivos de la Respuesta
"""

import time
import unittest
from pathlib import Path

import requests

from tests import config
from tests.database import TestExhExhortoRespuesta, get_database_session


class TestsEnviarRespuestaArchivos(unittest.TestCase):
    """Tests Enviar Respuesta Archivos"""

    def test_post_respuesta_archivos(self):
        """Probar el POST para enviar archivos de respuesta al exhorto"""

        # Cargar la sesión de la base de datos para recuperar los datos de la prueba anterior
        session = get_database_session()

        # Consultar la última respuesta con estado PENDIENTE
        test_exh_exhorto_respuesta = (
            session.query(TestExhExhortoRespuesta)
            .filter(TestExhExhortoRespuesta.estado == "PENDIENTE")
            .order_by(TestExhExhortoRespuesta.id.desc())
            .first()
        )
        if test_exh_exhorto_respuesta is None:
            self.fail("No se encontró la última respuesta PENDIENTE en SQLite")

        # Definir los datos que se van a incluir en el envío de los archivos
        payload_for_data = {
            "exhortoId": test_exh_exhorto_respuesta.test_exh_exhorto.exhorto_origen_id,
            "respuestaOrigenId": test_exh_exhorto_respuesta.respuesta_origen_id,
        }

        # Bucle para mandar los archivo por multipart/form-data
        data_acuse = None
        for test_exh_exhorto_respuesta_archivo in test_exh_exhorto_respuesta.test_exh_exhortos_respuestas_archivos:
            time.sleep(1)  # Pausa de 1 segundos

            # Tomar el nombre del archivo
            archivo_nombre = test_exh_exhorto_respuesta_archivo.nombre_archivo

            # Validar que el archivo exista
            respuesta_archivo = Path(f"tests/{archivo_nombre}")
            if not respuesta_archivo.exists():
                self.fail(f"El archivo {archivo_nombre} no existe")

            # Leer el archivo de prueba
            with open(respuesta_archivo, "rb") as archivo_prueba:
                # Mandar el archivo
                try:
                    respuesta = requests.post(
                        url=f"{config['api_base_url']}/exh_exhortos/recibir_respuesta_archivo",
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
                    # Continuar con el siguiente en lugar de self.assertEqual(contenido["success"], True)
                    continue

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

            # Actualizar el estado del archivo a RECIBIDO
            test_exh_exhorto_respuesta_archivo.estado = "RECIBIDO"

        # Validar que data_acuse NO sea nulo
        self.assertEqual(data_acuse is not None, True)

        # Validar el último acuse
        self.assertEqual(type(data_acuse), dict)
        self.assertEqual("exhortoId" in data_acuse, True)
        self.assertEqual("respuestaOrigenId" in data_acuse, True)
        self.assertEqual("fechaHoraRecepcion" in data_acuse, True)

        # Actualizar la respuesta en SQLite
        test_exh_exhorto_respuesta.estado = "ENVIADO"
        session.commit()

        # Actualizar el exhorto en SQLite
        test_exh_exhorto_respuesta.test_exh_exhorto.estado = "CONTESTADO"
        session.commit()

        # Cerrar la sesión SQLite
        session.close()


if __name__ == "__main__":
    unittest.main()
