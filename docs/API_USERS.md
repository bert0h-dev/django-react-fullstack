# API - Users Module

Documentación oficial para el módulo de **Users** en el sistema.

## 💼 Funcionalidades disponibles

- Crear usuarios
- Listar usuarios
- Ver detalle de usuario
- Actualizar información de usuario
- Eliminar usuarios

Todas las operaciones están protegidas por autenticación JWT y permisos de Admin o Staff.

## 🔑 Seguridad

**Autenticación:** JWT (Bearer Token en headers)

**Permisos:**

- Solo Admins o Staff (`IsAdminOrStaff`) pueden acceder a estos endpoints.

## 🔗 Endpoints de Users

### 1. Listar usuarios

**GET** `/api/accounts/users/`

Parámetros disponibles para filtros:

| Parámetro             | Tipo      | Descripción                                                   |
|-----------------------|-----------|---------------------------------------------------------------|
| `email`               | string    | Email del usuario                                             |
| `username`            | string    | Nombre del usuario                                            |
| `first_name`          | string    | Nombre                                                        |
| `last_name`           | string    | Apellido                                                      |
| `user_type`           | string    | Tipo de usuario                                               |
| `is_active`           | bool      | Estado activo                                                 |
| `last_activity`       | datetime  | Fecha de ultima actividad (UTC)                               |
| `last_activity_local` | datetime  | Fecha de ultima actividad segun la zona horaria del usuario.  |
| `timezone`            | datetime  | Timezone del usuario (default: America/Mexico_City)           |

### 2. Ver detalle de usuario

**GET** `/api/accounts/users/{id}/`

Devuelve la información de un usuario específico.

### 3. Crear usuario

**POST** `/api/accounts/users/`

Request:
```json
{
  "email": "nuevo@example.com",
  "username": "nuevousuario",
  "password": "Password123",
  "first_name": "Nuevo",
  "last_name": "Usuario",
  "user_type": "user"
}
```

Response:
```json
{
  "status": "success",
  "message": "Usuario creado correctamente",
  "http_code": 201,
  "data": { ...usuario creado... }
}
```

### 4. Actualizar usuario

**PATCH** `/api/accounts/users/{id}/`

Request de ejemplo:
```json
{
  "first_name": "Actualizado",
  "last_name": "Usuario"
}
```

### 5. Eliminar usuario

**DELETE** `/api/accounts/users/{id}/`

Elimina un usuario específico de manera segura.

## 📅 Estructura de un usuario

| Campo         | Tipo    | Descripción                                |
|---------------|---------|--------------------------------------------|
| `id`          | int     | ID del usuario                            |
| `email`       | string  | Email                                     |
| `username`    | string  | Username                                 |
| `first_name`  | string  | Primer nombre                            |
| `last_name`   | string  | Apellido                                 |
| `user_type`   | string  | admin / user                             |
| `is_active`   | bool    | Si el usuario está activo                 |
| `is_verified` | bool    | Si el usuario está verificado             |
| `last_activity` | datetime | Última actividad                        |

## 🚀 Validaciones en Register

- Email único y con formato correcto.
- Username único.
- Nombre y apellido solo letras.
- Password segura.
- Creación de tokens JWT automática al registrar.

## 📈 Respuestas estandarizadas

Todas las respuestas del módulo siguen el formato de `api_success` o `api_error`:

```json
{
  "status": "success",
  "message": "Acción realizada exitosamente",
  "http_code": 200,
  "data": { ... }
}
```

o en caso de error:

```json
{
  "status": "error",
  "message": "Detalle del error",
  "http_code": 400,
  "data": {}
}
```

## 🌐 Estado actual

Módulo de usuarios 100% operativo:

- CRUD completo
- Protegido
- Filtrado
- Paginado
- Logueado en AccessLogs

## Fin del documento
