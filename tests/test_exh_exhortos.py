"""
Unit test for exhortos category
"""

import unittest
import uuid
import requests
from tests.load_env import config


class TestExhExhortos(unittest.TestCase):
    """Tests for exh_exhortos category"""

    def test_get_exh_exhortos(self):
        """Test GET method for exh_exhortos"""
        response = requests.get(
            f"{config['api_base_url']}/exh_exhortos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_exh_exhorto_by_id(self):
        """Test GET method for exh_exhorto by id"""
        response = requests.get(
            f"{config['api_base_url']}/exh_exhortos/1",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        self.assertEqual(data["data"]["id"], 1)

    def test_post_exh_exhorto(self):
        """Test POST method for exh_exhorto"""
        random_uuid = uuid.uuid4()
        datos_nuevo_exhorto = {
            "exhortoOrigenId": str(random_uuid),
            "municipioDestinoId": 30,
            "materiaClave": "FAM",
            "estadoOrigenId": 19,
            "municipioOrigenId": 39,
            "juzgadoOrigenId": "NL-J2-FAM",
            "juzgadoOrigenNombre": "JUZGADO SEGUNDO FAMILIAR",
            "numeroExpedienteOrigen": "123/2024",
            "numeroOficioOrigen": "3001/2024",
            "tipoJuicioAsuntoDelitos": "DIVORCIO",
            "juezExhortante": "PEDRO INFANTE",
            "partes": [
                {
                    "nombre": "MARIA",
                    "apellidoPaterno": "FELIX",
                    "apellidoMaterno": "ALCALA",
                    "genero": "F",
                    "esPersonaMoral": False,
                    "tipoParte": 1,
                    "tipoParteNombre": "",
                },
                {
                    "nombre": "EULALIO",
                    "apellidoPaterno": "GONZALEZ",
                    "apellidoMaterno": "PIPORRO",
                    "genero": "M",
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
            "archivos": [{"nombreArchivo": "prueba.pdf", "hashSha1": "ABC123", "hashSha256": "ABC123", "tipoDocumento": 1}],
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
        self.assertEqual(data["data"]["exhortoOrigenId"], "XXX")


if __name__ == "__main__":
    unittest.main()
