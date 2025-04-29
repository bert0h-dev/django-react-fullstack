# CHANGELOG

Todas las modificaciones significativas de este proyecto se documentarán en este archivo.

El formato sigue el estándar [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y las versiones siguen [SemVer](https://semver.org/spec/v2.0.0.html).

## Inicial

- Inicialización de app `accounts` para manejo de usuarios.
- Inicialización de app `core` para logs de acceso y utilidades globales.
- Implementación de autenticación JWT (login, logout, refresh).
- Listado y filtrado de usuarios.
- Middleware de actualización automática de `last_activity` y `last_ip`.
- Sistema de logs de acceso automático en vistas.
- Exportaciones de logs en CSV, Excel, JSON y XML.
- Dockerización inicial (Dockerfile + docker-compose).
- Makefile para administración rápida de comandos.
- Integración de CI/CD con GitHub Actions.
- Documentación OpenAPI completa (Swagger UI).

## [v1.0.1] - 2024-05-01

### Agregado en v1.0.1

- CRUD completo de Roles (`RoleViewSet`).
- Endpoint para asignar permisos directos a usuarios (`assign-permissions`).
- Endpoint para asignar roles directos a usuarios (`assign-role`).

### Mejorado en v1.0.1

- Integración de `ListFilterOnlyMixin` para filtros inteligentes en listados.
- Documentación Swagger por operación (`list`, `retrieve`, `create`, `update`, `delete`).
- Se crearon carpetas de Serializer, Views, Urls donde se centraliza la información separado por proceso para tener un orden mas claro.

### Corregido en v1.0.1

- Validación para evitar eliminación de roles en uso.

### Eliminado en v1.0.1

- Se eliminaron los archivos urls.py, view.py y serializer.py de las apps `accounts` y `core`.

## [1.0.0] - 2024-04-28

### Agregado en v1.0.0

- Versión inicial estable del sistema backend.
- Entornos separados para desarrollo y producción.
- Testeos básicos de autenticación y usuarios.
- Integración multilenguaje (i18n) en backend.
