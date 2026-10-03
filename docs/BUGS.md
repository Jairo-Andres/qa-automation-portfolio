# Bugs y comportamientos inesperados encontrados

Durante las pruebas de la API [restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html) se detectaron los siguientes problemas.
Los tests de la colección están escritos para **documentar** el comportamiento real sin ocultarlo (cada uno tiene un comentario que apunta aquí).

---

### BUG-01 · Crear reserva con datos incompletos devuelve `500` en vez de `400`

| Campo | Valor |
|---|---|
| Severidad | Media |
| Endpoint | `POST /booking` |
| Pasos | Enviar un body que solo tenga `{"firstname": "SoloNombre"}` |
| Resultado esperado | `400 Bad Request` con un mensaje que indique qué campos faltan |
| Resultado obtenido | `500 Internal Server Error` |
| Impacto | El cliente no sabe qué ha hecho mal; un error de validación se trata como un fallo del servidor |

---

### BUG-02 · `DELETE /booking/{id}` devuelve `201 Created`

| Campo | Valor |
|---|---|
| Severidad | Baja |
| Endpoint | `DELETE /booking/{id}` |
| Resultado esperado | `200 OK` o `204 No Content` |
| Resultado obtenido | `201 Created` |
| Impacto | Semántica HTTP incorrecta; puede confundir a los clientes que validen el código de estado |

---

### BUG-03 · Login con credenciales incorrectas devuelve `200 OK`

| Campo | Valor |
|---|---|
| Severidad | Baja |
| Endpoint | `POST /auth` |
| Resultado esperado | `401 Unauthorized` |
| Resultado obtenido | `200 OK` con el body `{"reason": "Bad credentials"}` |
| Impacto | Los clientes tienen que leer el body para saber si el login falló |

---

### OBS-01 · `GET /ping` devuelve `201 Created`

Un health check debería devolver `200 OK`. No es grave, pero es otra inconsistencia en los códigos de estado.
