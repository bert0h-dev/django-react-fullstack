# API - Exportación de Access Logs

Documentación oficial para el módulo de **Access Log Export** del sistema.

## Endpoints disponibles

### 1. Listar Access Logs

**GET** `/api/core/access-logs/`

Permite listar todos los registros de acceso existentes.

Parámetros disponibles para filtros:

| Parámetro         | Tipo    | Descripción                                |
|--------------------|---------|--------------------------------------------|
| `user`             | int     | ID del usuario                             |
| `method`           | string  | Método HTTP (GET, POST, etc.)               |
| `status_code`      | int     | Código de respuesta HTTP                    |
| `action`           | string  | Contiene texto de la acción                 |
| `path`             | string  | Contiene texto del path                     |
| `created_at__gte`  | string  | Desde fecha y hora (YYYY-MM-DDTHH:MM)        |
| `created_at__lte`  | string  | Hasta fecha y hora (YYYY-MM-DDTHH:MM)        |

---

### 2. Ver detalle de Access Log

**GET** `/api/core/access-logs/{id}/`

Devuelve el detalle de un registro de acceso específico.

### 3. Exportar Access Logs

**GET** `/api/core/access-logs/export/`

Permite exportar los registros de acceso filtrados en diferentes formatos.

**Parámetros de exportación:**

| Parámetro         | Tipo    | Descripción                                |
|--------------------|---------|--------------------------------------------|
| `format`           | string  | Formato de exportación (`csv`, `xlsx`, `json`, `xml`) (default: csv) |
| `user`             | int     | ID del usuario                             |
| `method`           | string  | Método HTTP (GET, POST, etc.)               |
| `status_code`      | int     | Código de respuesta HTTP                    |
| `action`           | string  | Contiene texto de la acción                 |
| `path`             | string  | Contiene texto del path                     |
| `created_at__gte`  | string  | Desde fecha y hora (YYYY-MM-DDTHH:MM)        |
| `created_at__lte`  | string  | Hasta fecha y hora (YYYY-MM-DDTHH:MM)        |

**Ejemplos de exportación:**

- CSV: `/api/core/access-logs/export/?format=csv`
- Excel: `/api/core/access-logs/export/?format=xlsx`
- JSON: `/api/core/access-logs/export/?format=json`
- XML: `/api/core/access-logs/export/?format=xml`

**Notas:**

- Los filtros aplican igual que en el listado.
- Sólo usuarios con permisos de Admin o Staff pueden acceder a este recurso.

## Seguridad

Todos los endpoints requieren:

- **Autenticación JWT**
- **Usuario con permisos de Admin o Staff**

## 📊 Estructura de un registro de Access Log

| Campo         | Tipo    | Descripción                                 |
|---------------|---------|---------------------------------------------|
| `id`          | int     | ID del log                                  |
| `user`        | int     | ID del usuario (opcional si null)           |
| `user_email`  | string  | Email del usuario (opcional)                |
| `method`      | string  | Método HTTP                                 |
| `path`        | string  | Path consumido                              |
| `action`      | string  | Acción realizada                            |
| `status_code` | int     | Código de respuesta HTTP                    |
| `message`     | string  | Mensaje de la acción                        |
| `ip_address`  | string  | IP del cliente                              |
| `user_agent`  | string  | User Agent del cliente                      |
| `object_id`   | int     | ID del objeto                               |
| `object_type` | string  | Modelo completo consumido                   |
| `created_at`  | datetime| Fecha y hora de creación del log            |

## 🚀 Resumen

- Listar, ver detalle y exportar registros de acceso.
- Exportación disponible en CSV, Excel, JSON, XML.
- Protegido con autenticación y permisos.
- Filtros detallados para búsqueda específica.

---

💡 **Tip:** Integrar exportación en frontend o descargar directo desde Postman/Swagger.