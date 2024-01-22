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
    "errors": "Success",
    "total": 2812,
    "data": [
        {
            "id": 123,
            ...
        },
        ...
    ],
    "limit": 100,
    "offset": 0
}
```

En cambio, la respuesta que entrega un registro es:

```json
{
    "success": true,
    "message": "Success",
    "errors": "Success",
    "id": 123,
    ...
}
```

### Respuesta fallida por un registro no encontrado

Cuando NO se encuentra un registro el **status code** es **200** pero el **success** es Falso y el **message** describre el problema.

```json
{
  "success": false,
  "message": "No existe el registro"
}
```

### Respuesta fallida por ruta incorrecta

Cuando la ruta NO existe, simplemente ocurre un **status code** con error **404**.
