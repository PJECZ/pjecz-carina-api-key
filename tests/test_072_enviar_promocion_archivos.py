"""
Unit test - Enviar Archivos de la Promoción
"""

import time
import unittest
from pathlib import Path

import requests

from tests import config
from tests.database import ExhExhorto, ExhExhortoPromocion, get_database_session


class TestsEnviarArchivosPromocion(unittest.TestCase):
    """Tests Enviar Archivos de la Promoción"""

    def test_post_archivos_promocion(self):
        """Probar el POST para enviar archivos de una promoción"""

        # Cargar la sesión de la base de datos para recuperar los datos de la prueba anterior
        session = get_database_session()

        # Consultar el último exhorto
        exh_exhorto = session.query(ExhExhorto).order_by(ExhExhorto.id.desc()).first()
        if exh_exhorto is None:
            self.fail("No se encontró el último exhorto en database.sqlite")

        # Consultar la promoción del exhorto
        exh_exhorto_promocion = (
            session.query(ExhExhortoPromocion)
            .join(ExhExhorto)
            .filter(ExhExhorto.id == exh_exhorto.id)
            .order_by(ExhExhortoPromocion.id.desc())
            .first()
        )

        # Validar que exista la promoción
        if exh_exhorto_promocion is None:
            self.fail("No hay promoción POR ENVIAR en el exhorto")

        # Definir los datos que se van a incluir en el envío de los archivos
        payload_for_data = {
            "folioOrigenPromocion": exh_exhorto_promocion.folio_origen_promocion,
            "folioSeguimiento": exh_exhorto_promocion.folio_seguimiento,
        }

        # Bucle para mandar los archivos por multipart/form-data
        for exh_exhorto_promocion_archivo in exh_exhorto_promocion.exh_exhortos_promociones_archivos:
            time.sleep(2)  # Pausa de 2 segundos

            # Tomar el nombre del archivo
            archivo_nombre = exh_exhorto_promocion_archivo.nombre_archivo

            # Validar que el archivo exista
            archivo_ruta = Path(f"tests/{archivo_nombre}")
            if not archivo_ruta.is_file():
                self.fail(f"No se encontró el archivo {archivo_nombre}")

            # Leer el archivo de prueba
            with open(f"tests/{archivo_nombre}", "rb") as archivo_prueba:
                # Mandar el archivo
                try:
                    respuesta = requests.post(
                        url=f"{config['api_base_url']}/exh_exhortos/recibir_promocion_archivo",
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

                # Validar que dentro de archivo venga nombreArchivo
                self.assertEqual(type(data_archivo), dict)
                self.assertEqual("nombreArchivo" in data_archivo, True)

        # Validar el último acuse
        self.assertEqual(type(data_acuse), dict)
        self.assertEqual("folioOrigenPromocion" in data_acuse, True)
        self.assertEqual("folioPromocionRecibida" in data_acuse, True)
        self.assertEqual("fechaHoraRecepcion" in data_acuse, True)

        # Actualizar SQLite
        exh_exhorto_promocion_archivo.estado = "RECIBIDO"
        session.commit()


if __name__ == "__main__":
    unittest.main()
