"""
Settings

Para que la configuración no sea estática en el código,
se utiliza la librería pydantic para cargar la configuración desde
Google Secret Manager como primer opción, luego de un archivo .env
que se usa en local y por último de variables de entorno.

Para desarrollo debe crear un archivo .env en la raíz del proyecto
con las siguientes variables:

- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASS
- ORIGINS
- SALT

Para producción vaya a Google Secret Manager en
https://console.cloud.google.com/security/secret-manager
y cree como secretos las siguientes variable de entorno

- pjecz_carina_api_key_db_host
- pjecz_carina_api_key_db_port
- pjecz_carina_api_key_db_name
- pjecz_carina_api_key_db_user
- pjecz_carina_api_key_db_pass
- pjecz_carina_api_key_origins
- pjecz_carina_api_key_salt

Y en el archivo app.yaml agregue las siguientes variables de entorno

- PROJECT_ID: justicia-digital-gob-mx
- SERVICE_PREFIX: pjecz_carina_api_key
"""
import os
from functools import lru_cache

from google.cloud import secretmanager
from pydantic_settings import BaseSettings

PROJECT_ID = os.getenv("PROJECT_ID", "")  # Por defecto esta vacio, esto significa estamos en modo local
SERVICE_PREFIX = os.getenv("SERVICE_PREFIX", "pjecz_carina_api_key")


def get_secret(secret_id: str) -> str:
    """Get secret from google cloud secret manager"""

    # If not in google cloud, return environment variable
    if PROJECT_ID == "":
        return os.getenv(secret_id.upper(), "")

    # Create the secret manager client
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    secret = f"{SERVICE_PREFIX}_{secret_id}"
    name = client.secret_version_path(PROJECT_ID, secret, "latest")

    # Access the secret version
    response = client.access_secret_version(name=name)

    # Return the decoded payload
    return response.payload.data.decode("UTF-8")


class Settings(BaseSettings):
    """Settings"""

    db_host: str = get_secret("db_host")
    db_port: int = get_secret("db_port")
    db_name: str = get_secret("db_name")
    db_pass: str = get_secret("db_pass")
    db_user: str = get_secret("db_user")
    origins: str = get_secret("origins")
    salt: str = get_secret("salt")
    tz: str = "America/Mexico_City"

    class Config:
        """Load configuration"""

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Customise sources, first environment variables, then .env file, then google cloud secret manager"""
            return env_settings, file_secret_settings, init_settings


@lru_cache()
def get_settings() -> Settings:
    """Get Settings"""
    return Settings()
