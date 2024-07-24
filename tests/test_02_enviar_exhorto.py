"""
Unit test - 02 Enviar Exhorto
"""

import random
import unittest

import requests
from faker import Faker
from requests.exceptions import ConnectionError

from lib.pwgen import generar_identificador
from tests.database import ExhExhorto, ExhExhortoArchivo, get_database_session
from tests.load_env import config


class Test02EnviarExhorto(unittest.TestCase):
    """Test 02 Enviar Exhorto"""

    def test_post_exh_exhorto(self):
        """Probar el metodo POST para enviar un exhorto"""

        # Generar el exhorto_origen_id como el identificador del exhorto del PJ exhortante
        exhorto_origen_id = generar_identificador()

        # Inicializar el generardo de nombres aleatorios
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
        for numero in range(1, random.randint(1, 4) + 1):
            archivos.append(
                {
                    "nombreArchivo": f"prueba-{numero}.pdf",
                    "hashSha1": "3a9a09bbb22a6da576b2868c4b861cae6b096050",
                    "hashSha256": "df3d983d24a5002e7dcbff1629e25f45bb3def406682642643efc4c1c8950a77",
                    "tipoDocumento": 1,
                }
            )

        # TODO: Elegir un estado aleatoriamente

        # Definir los datos del exhorto
        datos = {
            "exhortoOrigenId": exhorto_origen_id,
            "municipioDestinoId": 30,
            "materiaClave": "FAM",
            "estadoOrigenId": 19,
            "municipioOrigenId": 39,
            "juzgadoOrigenId": "NL-J2-FAM",
            "juzgadoOrigenNombre": "JUZGADO SEGUNDO FAMILIAR",
            "numeroExpedienteOrigen": "123/2024",
            "numeroOficioOrigen": "3001/2024",
            "tipoJuicioAsuntoDelitos": "DIVORCIO",
            "juezExhortante": nombre_juez_exhortante,
            "partes": partes,
            "fojas": 41,
            "diasResponder": 15,
            "tipoDiligenciacionNombre": "OFICIO",
            "fechaOrigen": "2024-05-03T21:58:45.258Z",
            "observaciones": "CELEBRIDADES QUE SE VAN A DIVORCIAR",
            "archivos": archivos,
        }

        # Mandar el exhorto
        try:
            respuesta = requests.post(
                url=f"{config['api_base_url']}/exh_exhortos",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
                json=datos,
            )
        except ConnectionError as error:
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

        # Validar que dentro de data venga exhortoOrigenId y fechaHora
        self.assertEqual("exhortoOrigenId" in data, True)
        self.assertEqual("fechaHora" in data, True)

        # Validar que nos regrese el mismo exhorto_origen_id
        self.assertEqual(data["exhortoOrigenId"], exhorto_origen_id)

        # Cargar la sesion de la base de datos para conservar los datos para las pruebas siguientes
        session = get_database_session()

        # Guardar el exhorto
        exh_exhorto = ExhExhorto(
            exhorto_origen_id=exhorto_origen_id,
            folio_seguimiento=data["exhortoOrigenId"],
        )
        session.add(exh_exhorto)
        session.commit()

        # Guardar los archivos
        for archivo in archivos:
            exh_exhorto_archivo = ExhExhortoArchivo(
                exh_exhorto_id=exh_exhorto.id,
                exh_exhorto=exh_exhorto,
                nombre_archivo=archivo["nombreArchivo"],
                hash_sha1=archivo["hashSha1"],
                hash_sha256=archivo["hashSha256"],
                tipo_documento=archivo["tipoDocumento"],
            )
            session.add(exh_exhorto_archivo)
            session.commit()


if __name__ == "__main__":
    unittest.main()
