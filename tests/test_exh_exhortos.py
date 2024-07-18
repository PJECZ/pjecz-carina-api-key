"""
Unit test for exhortos category
"""

import random
import time
import unittest

import requests
from faker import Faker

from lib.pwgen import generar_identificador
from tests.load_env import config


class TestExhExhortos(unittest.TestCase):
    """Tests for exh_exhortos category"""

    def test_post_exh_exhorto(self):
        """Test POST method for exh_exhorto"""

        # Generar exhortoOrigenId
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

        # Generar de 1 a 4 archivos de prueba
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
        exhorto_response = requests.post(
            url=f"{config['api_base_url']}/exh_exhortos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
            json=datos_nuevo_exhorto,
        )
        exhorto_res_json = exhorto_response.json()
        if "success" in exhorto_res_json:
            if exhorto_res_json["success"] is False:
                if "message" in exhorto_res_json:
                    print("MENSAJE: ", exhorto_res_json["message"])
                if "errors" in exhorto_res_json:
                    print("ERRORES: ", exhorto_res_json["errors"])
            self.assertEqual(exhorto_res_json["success"], True)
        else:
            self.assertEqual(exhorto_response.status_code, 200)

        # Mandar un archivo multipart/form-data
        for archivo in archivos:
            time.sleep(2)  # Pausa de 2 segundos
            archivo_prueba_nombre = archivo["nombreArchivo"]
            with open(f"tests/{archivo_prueba_nombre}", "rb") as archivo_prueba:
                archivo_response = requests.post(
                    url=f"{config['api_base_url']}/exh_exhortos_archivos/upload",
                    headers={"X-Api-Key": config["api_key"]},
                    timeout=config["timeout"],
                    params={"exhortoOrigenId": exhorto_origen_id},
                    files={"archivo": (archivo_prueba_nombre, archivo_prueba, "application/pdf")},
                )
                archivo_res_json = archivo_response.json()
                if "success" in archivo_res_json:
                    if archivo_res_json["success"] is False:
                        if "message" in archivo_res_json:
                            print("MENSAJE: ", archivo_res_json["message"])
                        if "errors" in archivo_res_json:
                            print("ERRORES: ", archivo_res_json["errors"])
                    self.assertEqual(archivo_res_json["success"], True)
                else:
                    self.assertEqual(archivo_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
