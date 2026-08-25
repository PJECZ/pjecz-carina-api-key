# pjecz-carina-api-key

API con autentificación para enviar y recibir exhortos.

## Requerimientos

Los requerimientos son

- Python 3.14
- PostgreSQL 15 o superior

## Instalación

Crear el entorno virtual

```bash
python3.11 -m venv .venv
```

Ingresar al entorno virtual

```bash
source .venv/bin/activate
```

Actualizar el gestor de paquetes **pip**

```bash
pip install --upgrade pip
```

Usar **uv** para instalar las dependencias

```bash
uv sync
```

## Configuración

Crear un archivo `.env` en la raíz del proyecto con las variables de entorno

```ini
# Base de datos
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=pjecz_plataforma_web
DB_USER=XXXXXXXXXXXX
DB_PASS=XXXXXXXXXXXX

# Google Cloud Storage
CLOUD_STORAGE_DEPOSITO=XXXXXXXXXXXX

# Clave INEGI del Estado, 05 = Coahuila de Zaragoza
ESTADO_CLAVE=05

# Origins
ORIGINS=http://127.0.0.1:3000

# Salt sirve para cifrar el ID con HashID
SALT=XXXXXXXXXXXX
```

Crear un archivo `.bashrc` que cargue las variables de entorno y el entorno virtual

```bash
if [ -f ~/.bashrc ]
then
    . ~/.bashrc
fi

if command -v figlet &> /dev/null
then
    figlet Carina API key
else
    echo "== Carina API key"
fi
echo

if [ -f .env ]
then
    echo "-- Variables de entorno"
    export $(grep -v '^#' .env | xargs)
    # source .env && export $(sed '/^#/d' .env | cut -d= -f1)
    echo "   CLOUD_STORAGE_DEPOSITO: ${CLOUD_STORAGE_DEPOSITO}"
    echo "   DB_HOST: ${DB_HOST}"
    echo "   DB_PORT: ${DB_PORT}"
    echo "   DB_NAME: ${DB_NAME}"
    echo "   DB_USER: ${DB_USER}"
    echo "   DB_PASS: ${DB_PASS}"
    echo "   ESTADO_CLAVE: ${ESTADO_CLAVE}"
    echo "   ORIGINS: ${ORIGINS}"
    echo "   SALT: ${SALT}"
    echo
    export PGHOST=$DB_HOST
    export PGPORT=$DB_PORT
    export PGDATABASE=$DB_NAME
    export PGUSER=$DB_USER
    export PGPASSWORD=$DB_PASS
fi

if [ -d .venv ]
then
    echo "-- Python Virtual Environment"
    source .venv/bin/activate
    echo "   $(python3 --version)"
    export PYTHONPATH=$(pwd)
    echo "   PYTHONPATH: ${PYTHONPATH}"
    echo
    echo "-- FastAPI 127.0.0.1:8000"
    alias arrancar="uvicorn --host=127.0.0.1 --port 8000 --reload pjecz_carina_api_key.main:app"
    echo "   arrancar"
    echo
    if [ -d tests ]
    then
        echo "-- Pruebas unitarias"
        echo "   python3 -m unittest discover"
        echo
    fi
fi
```

## Arrancar

Cargar las variables de entorno y el entorno virtual

```bash
source .bashrc
```

Lanzar **FastAPI** por medio del _alias_ que se cargó en el `source .bashrc`

```bash
arrancar
```
