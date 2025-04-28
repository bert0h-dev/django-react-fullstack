# Proyecto Fullstack - Sistema de Autenticación y Auditoría

Bienvenido al proyecto Fullstack basado en Django Rest Framework + PostgreSQL + Swagger + JWT Authentication.

Este sistema fue diseñado como una base sólida para aplicaciones empresariales, médicas, financieras o de alta auditoría.

## 🔖 Tecnologías principales

- **Python 3.11**
- **Django 4.x**
- **Django Rest Framework (DRF)**
- **PostgreSQL**
- **SimpleJWT** (manejo de tokens de acceso y refresh)
- **drf-spectacular** (documentación OpenAPI/Swagger)
- **Django Filters** (para búsquedas y filtros avanzados)
- **Openpyxl** (exportación Excel)

## 📖 Módulos actuales

| Módulo       | Descripción                                                   |
|--------------|---------------------------------------------------------------|
| **Accounts** | Manejo de usuarios: login, logout, registro, CRUD de usuarios |
| **Core**     | Logs de acceso, exportaciones, permisos globales, utilidades  |

## 📌 Características

- Autenticación JWT (Access + Refresh Tokens)
- API REST 100% estandarizada (respuestas `api_success` / `api_error`)
- Actualización automática de `last_activity` y `last_ip` del usuario
- Acceso a logs de actividad por usuario, IP, fecha, acción, etc.
- Exportación de logs en formatos: CSV, Excel (XLSX), JSON, XML
- Soporte multilenguaje (`gettext_lazy`)
- Paginación y filtros avanzados en listados
- Seguridad avanzada basada en roles (`IsAdminOrStaff`)
- Documentación Swagger UI auto-generada
- Tests unitarios integrados

## 🔒 Endpoints principales

| Acción             | Endpoint |
|--------------------|----------------------------------|
| Login              | `/api/accounts/login/`           |
| Refresh Token      | `/api/accounts/token/refresh/`   |
| Logout             | `/api/accounts/logout/`          |
| CRUD Usuarios      | `/api/accounts/users/`           |
| Listar Access Logs | `/api/core/access-logs/`         |
| Exportar Logs      | `/api/core/access-logs/export/`  |

## 🔍 Instalación Rápida

1. Clona el repositorio
2. Crea y activa un entorno virtual
3. Instala las dependencias

```bash
pip install -r requirements.txt
```

4. Configura tu base de datos PostgreSQL en `settings.py`
5. Realiza migraciones

```bash
python manage.py migrate
```

6. Crea un superusuario

```bash
python manage.py createsuperuser
```

7. Corre el servidor

```bash
python manage.py runserver
```

Accede a la documentación Swagger en

```
http://localhost:8000/api/schema/swagger-ui/
```

## 🚀 Estado actual

Sistema 100% funcional en:

- Autenticación JWT
- Manejo de usuarios (registro, login, perfil)
- Logs de acceso
- Exportaciones de auditoría

## 🕺 Autor

Proyecto desarrollado por Humberto Morales (Bert0h-dev).

## 📚 Licencia

Uso libre para proyectos de aprendizaje, comerciales o empresariales. Se sugiere dar crédito al autor si se utiliza la base de este sistema para proyectos públicos.

## Fin del documento
