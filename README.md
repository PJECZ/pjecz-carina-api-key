# pjecz-carina-api-key

API con autentificación para enviar y recibir exhortos.

## Mejores prácticas usadas en esta API

Siguiendo las recomendaciones del artículo [I've been abusing HTTP Status Codes in my APIs for years](https://blog.slimjim.xyz/posts/stop-using-http-codes/) esta API responde siempre con un **success** que puede ser veradero o falso y un **message** con un texto de mensaje.

### Respuesta exitosa

Cuando el resultado es exitoso el **status code** es **200** y el **message** es **Success**.

La respuesta que entrega un _paginado_ de items tiene el total, el limit y el offset:

```json
{
    "success": true,
    "message": "Success",
    "errors": [],
    "data": [
        {
            "id": 123,
            ...
        },
        ...
    ],
}
```

En cambio, la respuesta que entrega un registro es:

```json
{
    "success": true,
    "message": "Success",
    "errors": [],
    "id": 123,
    ...
}
```

### Respuesta fallida por un registro no encontrado

Cuando NO se encuentra un registro el **status code** es **200** pero el **success** es Falso y el **message** describre el problema.

```json
{
  "success": false,
  "message": "",
  "errors": ["No existe el registro"]
}
```

### Respuesta fallida por ruta incorrecta

Cuando la ruta NO existe, simplemente ocurre un **status code** con error **404**.

## Instalación

Crear el entorno virtual

```bash
python3.11 -m venv .venv
```

Ingresar al entorno virtual

```bash
source venv/bin/activate
```

Actualizar el gestor de paquetes **pip**

```bash
pip install --upgrade pip
```

Instalar el paquete **wheel** para compilar las dependencias

```bash
pip install wheel
```

Instalar **poetry** en el entorno virtual si no lo tiene desde el sistema operativo

```bash
pip install poetry
```

Verificar que la configuracion `virtualenvs.in-project` sea True

```bash
poetry config virtualenvs.in-project
```

Si es falso, configurar **poetry** para que use el entorno virtual dentro del proyecto

```bash
poetry config virtualenvs.in-project true
```

Instalar los paquetes por medio de **poetry**

```bash
poetry install
```

## Configuracion

Crear un archivo `.env` con las variables de entorno

```ini
# Base de datos
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=pjecz_plataforma_web
DB_USER=adminpjeczplataformaweb
DB_PASS=XXXXXXXXXXXXXXXX

# Google Cloud Storage
CLOUD_STORAGE_DEPOSITO=pjecz-desarrollo

# Origins
ORIGINS=http://localhost:3000

# Salt sirve para cifrar el ID con HashID, debe ser igual en la API
SALT=XXXXXXXXXXXXXXXX
```

Crear un archivo `.bashrc`

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
    echo "   ORIGINS: ${ORIGINS}"
    echo "   SALT: ${SALT}"
    echo
    export PGHOST=$DB_HOST
    export PGPORT=$DB_PORT
    export PGDATABASE=$DB_NAME
    export PGUSER=$DB_USER
    export PGPASSWORD=$DB_PASS
fi
```

## Arrancar

Ejecute el `.bashrc` para entrar al entorno virtual y cargar las variables de entorno

```bash
. .bashrc
```

Para arrancar el servidor ejecute

```bash
arrancar
```
