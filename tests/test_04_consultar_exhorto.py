"""
Unit test - 04 Consultar Exhorto
"""

import unittest

import requests

from tests.database import ExhExhorto, get_database_session
from tests.load_env import config


class Test04ConsultarExhorto(unittest.TestCase):
    """Test 04 Consultar Exhorto"""

    def test_get_exh_exhortos(self):
        """Probar el metodo GET para consultar un exhorto"""

        # Cargar la sesion de la base de datos para recuperar los datos
        session = get_database_session()

        # Consultar el último exhorto
        exh_exhorto = session.query(ExhExhorto).order_by(ExhExhorto.id.desc()).first()
        if exh_exhorto is None:
            self.fail("No se encontró el último exhorto en database.sqlite")

        # Validar que exh_exhorto.folio_seguimiento sea string y que no este vacio
        self.assertIsInstance(exh_exhorto.folio_seguimiento, str)
        self.assertNotEqual(exh_exhorto.folio_seguimiento, "")

        # Consultar el exhorto
        try:
            respuesta = requests.get(
                url=f"{config['api_base_url']}/exh_exhortos/{exh_exhorto.folio_seguimiento}",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
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

        # Validar el contenido de data
        self.assertEqual("exhortoOrigenId" in data, True)
        self.assertEqual("folioSeguimiento" in data, True)
        self.assertEqual("estadoDestinoId" in data, True)
        self.assertEqual("estadoDestinoNombre" in data, True)
        self.assertEqual("municipioDestinoId" in data, True)
        self.assertEqual("municipioDestinoNombre" in data, True)
        self.assertEqual("materiaClave" in data, True)
        self.assertEqual("materiaNombre" in data, True)
        self.assertEqual("estadoOrigenId" in data, True)
        self.assertEqual("estadoOrigenNombre" in data, True)
        self.assertEqual("municipioOrigenId" in data, True)
        self.assertEqual("municipioOrigenNombre" in data, True)
        self.assertEqual("juzgadoOrigenId" in data, True)
        self.assertEqual("juzgadoOrigenNombre" in data, True)
        self.assertEqual("numeroExpedienteOrigen" in data, True)
        self.assertEqual("numeroOficioOrigen" in data, True)
        self.assertEqual("tipoJuicioAsuntoDelitos" in data, True)
        self.assertEqual("juezExhortante" in data, True)
        self.assertEqual("partes" in data, True)
        self.assertEqual("fojas" in data, True)
        self.assertEqual("diasResponder" in data, True)
        self.assertEqual("tipoDiligenciacionNombre" in data, True)
        self.assertEqual("fechaOrigen" in data, True)
        self.assertEqual("observaciones" in data, True)
        self.assertEqual("archivos" in data, True)
        self.assertEqual("fechaHoraRecepcion" in data, True)
        self.assertEqual("municipioTurnadoId" in data, True)
        self.assertEqual("municipioTurnadoNombre" in data, True)
        self.assertEqual("areaTurnadoId" in data, True)
        self.assertEqual("areaTurnadoNombre" in data, True)
        self.assertEqual("numeroExhorto" in data, True)
        self.assertEqual("urlInfo" in data, True)
