# API - Documentación General del Proyecto Fullstack

Descripción completa del backend basado en Django Rest Framework con JWT, Swagger, PostgreSQL y modularizado en apps.

## 💼 Módulos implementados

- **Accounts** (Autenticación y manejo de usuarios)
- **Core** (Funciones comunes: logs de acceso, exportaciones, permisos globales)

## 🔑 Autenticación

**Autenticación:** Basada en JWT (access y refresh tokens)

## Endpoints principales

### 1. Login

**POST** `/api/accounts/login/`

Request:
```json
{
  "email": "usuario@example.com",
  "password": "Password123"
}
```

Response:
```json
{
  "status": "success",
  "message": "Inicio de sesión exitoso",
  "http_code": 200,
  "data": {
    "access": "...",
    "refresh": "...",
    "user": {
      "id": 1,
      "email": "usuario@example.com",
      "username": "usuario"
    }
  }
}
```

### 2. Refresh Token

**POST** `/api/accounts/token/refresh/`

Request:
```json
{
  "refresh": "..."
}
```

Response:
```json
{
  "status": "success",
  "message": "Token de acceso renovado correctamente",
  "http_code": 200,
  "data": {
    "access": "..."
  }
}
```

### 3. Logout

**POST** `/api/accounts/logout/`

Cierra sesión invalidando el refresh token.

---

## 👥 Manejo de Usuarios

## Endpoints disponibles

- **Listar usuarios:** `GET /api/accounts/users/`
- **Detalle usuario:** `GET /api/accounts/users/{id}/`
- **Crear usuario:** `POST /api/accounts/users/`
- **Actualizar usuario:** `PATCH /api/accounts/users/{id}/`
- **Eliminar usuario:** `DELETE /api/accounts/users/{id}/`

**Seguridad:** Solo Admins o Staff.

Campos de usuario manejados:

- Email
- Username
- First name
- Last name
- User Type (admin/user)
- Idioma preferido
- Timezone
- Estado de verificación
- IP y última actividad

## 📊 Access Logs

Sistema de auditoría de todas las acciones importantes realizadas por los usuarios.

## Endpoints de Access Logs

- **Listar logs:** `GET /api/core/access-logs/`
- **Detalle de log:** `GET /api/core/access-logs/{id}/`
- **Exportar logs:** `GET /api/core/access-logs/export/`

Formatos soportados para exportación:

- CSV
- Excel (XLSX)
- JSON
- XML

**Filtros disponibles:**

- Usuario
- Método HTTP (GET, POST, etc.)
- Status code
- Acción contiene texto
- Path contiene texto
- Rango de fechas (created_at__gte y created_at__lte)

## 🔒 Permisos implementados

- **IsAdminOrStaff:** Solo usuarios admin o staff pueden acceder a ciertas vistas.
- **Decorador log_view_action:** Log automático de acciones de vistas sensibles.

## 📅 Features extra

- Middleware que actualiza `last_activity` y `last_ip` automáticamente.
- Soporte multilenguaje (`gettext_lazy`) en campos y respuestas.
- Documentación completa de API con **drf-spectacular** (Swagger UI).
- Respuestas JSON estandarizadas (api_success y api_error).
- Tests unitarios para login, logout, refresh, CRUD de usuarios.
- Factories para generación de usuarios de prueba.
- Paginación y filtros avanzados en todos los listados.

## 🚀 Tecnologías usadas

- Python 3.11+
- Django 4.x
- Django Rest Framework (DRF)
- SimpleJWT
- drf-spectacular (Swagger/OpenAPI)
- PostgreSQL
- Openpyxl (Excel export)
- Django Filters

## 📖 Próximos pasos sugeridos

- Implementación de perfiles de Doctor y Paciente.
- Agendamiento de citas médicas.
- Enlace a sistemas de notificación.
- Log de actividades médicas.
- Dashboard administrativo.

## 🎉 Estado actual del sistema

- **"Base de autenticación y auditoría blindada, lista para crecimiento y escalamiento médico."**

### Fin del documento
