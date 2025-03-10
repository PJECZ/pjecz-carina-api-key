# Unit Tests

Obtenga el SHA1 y SHA256 de sus prueba-1.pdf

```bash
sha1sum tests/prueba-1.pdf
```

Crear un archivo .env con las siguientes variables

```ini
API_KEY=XXXXXXXX.XXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXX
API_BASE_URL=http://127.0.0.1:8000/v5
TIMEOUT=10
ESTADO_CLAVE=05
ARCHIVO_PDF_HASHSHA1=
ARCHIVO_PDF_HASHSHA256=
```

## Probar cuando el remitente es EXTERNO

Se usa la base de datos SQLite para pasar datos entre las pruebas

1. Pruebe `python3 -m unittest tests/test_010_consultar_materias.py`
2. Pruebe `python3 -m unittest tests/test_020_enviar_exhorto.py`
3. Pruebe `python3 -m unittest tests/test_030_enviar_exhorto_archivos.py`
4. Vaya a Plataforma Web cambie a TRANSFERIDO y luego a PROCESANDO
5. Simule que se manda la respuesta `cli exh_exhortos demo-05-enviar-respuesta XXXXXXXXXXX`
6. Pruebe `python3 -m unittest tests/test_060_enviar_actualizacion.py`
7. Pruebe `python3 -m unittest tests/test_071_enviar_promocion.py`
8. Pruebe `python3 -m unittest tests/test_072_enviar_promocion_archivos.py`

## Probar cuando el remitente es INTERNO

El **FOLIO_SEGUIMIENTO** se debe tener en las variables de entorno

1. Vaya a Plataforma Web y cree un exhorto
2. Agregue las partes
3. Agregue por lo menos un archivo
4. Copie el Exhorto Origen ID
5. Ejecute `cli exh_exhortos demo-02-enviar XXXXXXXXXXX`
6. Pruebe `python3 -m unittest tests/test_040_consultar_exhorto.py`
7. Pruebe `python3 -m unittest tests/test_051_enviar_respuesta.py`
8. Pruebe `python3 -m unittest tests/test_052_enviar_respuesta_archivos.py`
