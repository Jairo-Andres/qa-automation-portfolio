# QA Automation Portfolio

![Tests](https://github.com/Jairo-Andres/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg)

Proyecto de automatización de pruebas con dos partes:

| Parte | Herramientas | Aplicación bajo prueba |
|---|---|---|
| **UI / E2E** | Python · Playwright · pytest · Page Object Model | [saucedemo.com](https://www.saucedemo.com) (tienda online de demo) |
| **API REST** | Postman · Newman · JSON Schema | [restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html) (API de reservas de hotel) |

Los dos suites se ejecutan automáticamente con **GitHub Actions** en cada push y generan reportes HTML.

---

## Qué se prueba

### UI (15 tests)
- **Login:** acceso correcto y 4 casos negativos (usuario bloqueado, contraseña incorrecta, campos vacíos), usando tests parametrizados.
- **Carrito:** añadir uno o varios productos, verificar el contador y eliminar productos.
- **Checkout:** compra completa end-to-end y validación de campos obligatorios del formulario.
- **Ordenación:** por precio (ascendente y descendente) y por nombre (Z-A).

### API (16 peticiones · 28 aserciones)
- **Health check** y tiempo de respuesta.
- **Autenticación:** obtención de token y credenciales incorrectas.
- **Flujo CRUD encadenado:** crear → consultar → buscar → actualizar (PUT) → actualizar parcial (PATCH) → borrar → verificar 404. El `bookingid` y el token se pasan entre peticiones con variables.
- **Validación de esquema** JSON de la respuesta.
- **Casos negativos:** modificar sin token, borrar con token inválido, recurso inexistente y body incompleto.
- Datos de prueba **aleatorios** en cada ejecución (`$randomFirstName`…) para que las pruebas sean independientes.

🐞 Durante las pruebas se encontraron **3 bugs** en la API → ver [docs/BUGS.md](docs/BUGS.md).

---

## Estructura

```
├── ui-tests/
│   ├── pages/          # Page Objects (login, inventario, carrito, checkout)
│   ├── tests/          # tests de pytest
│   └── conftest.py     # fixtures (p. ej. usuario ya logueado)
├── api-tests/postman/  # colección y environment de Postman
├── docs/BUGS.md        # bugs encontrados
├── .github/workflows/  # pipeline de CI
├── pytest.ini          # configuración: navegador, capturas, trazas, reporte
└── package.json        # Newman para ejecutar la colección desde consola
```

---

## Cómo ejecutarlo

### Tests de UI
Requisitos: Python 3.10+

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (en Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
playwright install chromium
pytest
```

Opciones útiles:
```bash
pytest --headed --slowmo 500    # ver el navegador mientras se ejecuta
pytest -m smoke                 # solo los tests críticos
```

Reporte: `reports/ui-report.html`. Si un test falla, en `test-results/` se guardan la captura y la traza, que se puede abrir con `playwright show-trace <archivo.zip>`.

### Tests de API
Requisitos: Node.js 18+

```bash
npm install
npm run test:api
```

Reporte: `reports/api-report.html`.

También se puede importar la colección y el environment de `api-tests/postman/` en Postman y ejecutarla con el **Collection Runner**.

---

## Decisiones técnicas

- **¿Por qué Playwright y no Selenium?** Playwright tiene esperas automáticas (menos tests inestables), se integra de forma nativa con pytest y trae herramientas de depuración como Trace Viewer y Codegen. Selenium sigue siendo muy usado, pero para un proyecto nuevo Playwright es más rápido de montar y de mantener.
- **Page Object Model:** los selectores están en un solo sitio, así que si cambia la web solo hay que tocar la página correspondiente, no todos los tests.
- **Fixtures de pytest:** `inventory_page` deja al usuario ya logueado, lo que evita repetir el login en cada test.
- **Tests de API independientes:** cada ejecución crea sus propios datos y los borra al final.
