"""
Unit test for exhortos category
"""

import time
import unittest
import uuid
import random
import requests
from faker import Faker
from tests.load_env import config


class TestExhExhortos(unittest.TestCase):
    """Tests for exh_exhortos category"""

    def test_post_exh_exhorto(self):
        """Test POST method for exh_exhorto"""

        # Generar exhortoOrigenId
        random_uuid = uuid.uuid4()
        exhorto_origen_id = str(random_uuid)

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

        # Generar de 1 a 4 archivos de prueba
        archivos = []
        for numero in range(1, random.randint(1, 4) + 1):
            archivos.append(
                {
                    "nombreArchivo": f"prueba-{numero}.pdf",
                    "hashSha1": "",
                    "hashSha256": "",
                    "tipoDocumento": 1,
                }
            )

        # Mandar Exhorto
        datos_nuevo_exhorto = {
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
            "partes": [
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
            ],
            "fojas": 41,
            "diasResponder": 15,
            "tipoDiligenciacionNombre": "OFICIO",
            "fechaOrigen": "2024-05-03T21:58:45.258Z",
            "observaciones": "CELEBRIDADES QUE SE VAN A DIVORCIAR",
            "archivos": archivos,
        }
        response = requests.post(
            f"{config['api_base_url']}/exh_exhortos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
            json=datos_nuevo_exhorto,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        self.assertEqual(data["data"]["exhortoOrigenId"], exhorto_origen_id)

        # Mandar un archivo multipart/form-data
        for archivo in archivos:
            time.sleep(5)  # Pausa de 5 segundos
            archivo_prueba_nombre = archivo["nombreArchivo"]
            with open(f"tests/{archivo_prueba_nombre}", "rb") as archivo_prueba:
                response = requests.post(
                    f"{config['api_base_url']}/exh_exhortos_archivos/upload",
                    headers={"X-Api-Key": config["api_key"]},
                    timeout=config["timeout"],
                    params={"exhortoOrigenId": exhorto_origen_id},
                    files={"archivo": (archivo_prueba_nombre, archivo_prueba, "application/pdf")},
                )
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertEqual(data["success"], True)


if __name__ == "__main__":
    unittest.main()
