"""
Unit test - Enviar Exhorto
"""

import random
import unittest
from datetime import datetime

import requests
from faker import Faker

from pjecz_carina_api_key.dependencies.pwgen import generar_identificador
from tests import config
from tests.database import TestExhExhorto, TestExhExhortoArchivo, get_database_session


class TestsEnviarExhorto(unittest.TestCase):
    """Tests Enviar Exhorto"""

    def test_post_exhorto(self):
        """Probar el POST para enviar un exhorto"""

        # Generar el exhorto_origen_id como el identificador del exhorto del PJ exhortante
        exhorto_origen_id = generar_identificador()

        # Inicializar el generador de nombres aleatorios
        faker = Faker(locale="es_MX")

        # Generar el nombre del juez exhortante
        nombre_juez_exhortante = faker.name()

        # Generar la parte Actor(1) con nombres aleatorios
        if faker.random_element(elements=("M", "F")) == "F":
            nombre_actor = faker.first_name_female()
            genero_actor = "F"
        else:
            nombre_actor = faker.first_name_male()
            genero_actor = "M"
        apellido_paterno_actor = faker.last_name()
        apellido_materno_actor = faker.last_name()

        # Generar la parte Demandado(2) con nombres aleatorios
        if faker.random_element(elements=("M", "F")) == "F":
            nombre_demandado = faker.first_name_female()
            genero_demandado = "F"
        else:
            nombre_demandado = faker.first_name_male()
            genero_demandado = "M"
        apellido_paterno_demandado = faker.last_name()
        apellido_materno_demandado = faker.last_name()

        # Definir las partes
        partes = [
            {
                "nombre": nombre_actor,
                "apellidoPaterno": apellido_paterno_actor,
                "apellidoMaterno": apellido_materno_actor,
                "genero": genero_actor,
                "esPersonaMoral": False,
                "tipoParte": 1,
                "tipoParteNombre": "",
            },
            {
                "nombre": nombre_demandado,
                "apellidoPaterno": apellido_paterno_demandado,
                "apellidoMaterno": apellido_materno_demandado,
                "genero": genero_demandado,
                "esPersonaMoral": False,
                "tipoParte": 2,
                "tipoParteNombre": "",
            },
        ]

        # Inicializar los archivos que se van a mandar desde prueba-1.pdf a prueba-4.pdf
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

        # Elegir un estado de origen aleatorio
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/estados",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)
        contenido = response.json()
        estado = random.choice(contenido["data"])

        # Elegir un municipio de origen aleatorio
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/municipios/{estado['clave']}",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)
        contenido = response.json()
        municipio = random.choice(contenido["data"])

        # Definir un número de expediente y número de oficio aleatorio
        anio = datetime.now().year
        numero_expediente = f"{random.randint(1, 100)}/{anio}"
        numero_oficio = f"{random.randint(1, 100)}/{anio}"

        # Definir los datos del exhorto
        payload_for_json = {
            "exhortoOrigenId": exhorto_origen_id,
            "municipioDestinoId": 30,
            "materiaClave": "CIV",
            "estadoOrigenId": int(estado["clave"]),
            "municipioOrigenId": int(municipio["clave"]),
            "juzgadoOrigenId": "EDO-J2-FAM",
            "juzgadoOrigenNombre": "JUZGADO SEGUNDO FAMILIAR",
            "numeroExpedienteOrigen": numero_expediente,
            "numeroOficioOrigen": numero_oficio,
            "tipoJuicioAsuntoDelitos": "DIVORCIO",
            "juezExhortante": nombre_juez_exhortante,
            "partes": partes,
            "fojas": 41,
            "diasResponder": 15,
            "tipoDiligenciacionNombre": "OFICIO",
            "fechaOrigen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "observaciones": "CELEBRIDADES QUE SE VAN A DIVORCIAR",
            "archivos": archivos,
        }

        # Mandar el exhorto
        try:
            respuesta = requests.post(
                url=f"{config['api_base_url']}/exh_exhortos/recibir",
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

        # Validar que dentro de data venga exhortoOrigenId y fechaHora
        self.assertEqual("exhortoOrigenId" in data, True)
        self.assertEqual("fechaHora" in data, True)

        # Validar que nos regrese el mismo exhorto_origen_id
        self.assertEqual(data["exhortoOrigenId"], exhorto_origen_id)

        # Cargar la sesión de SQLite para conservar los datos para las pruebas siguientes
        session = get_database_session()

        # Insertar el exhorto en SQLite
        test_exh_exhorto = TestExhExhorto(
            exhorto_origen_id=exhorto_origen_id,
            folio_seguimiento=data["exhortoOrigenId"],
            estado_origen_id=int(estado["clave"]),
            estado="PENDIENTE",
        )
        session.add(test_exh_exhorto)
        session.commit()

        # Insertar los archivos del exhorto en SQLite
        for archivo in archivos:
            test_exh_exhorto_archivo = TestExhExhortoArchivo(
                test_exh_exhorto=test_exh_exhorto,
                test_exh_exhorto_id=test_exh_exhorto.id,
                nombre_archivo=archivo["nombreArchivo"],
                hash_sha1=archivo["hashSha1"],
                hash_sha256=archivo["hashSha256"],
                tipo_documento=archivo["tipoDocumento"],
            )
            session.add(test_exh_exhorto_archivo)
            session.commit()

        # Cerrar la sesión sqlite
        session.close()


if __name__ == "__main__":
    unittest.main()
