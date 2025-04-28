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

## [1.0.1] - 2024-04-28

### Agregado

- Versión inicial estable del sistema backend.
- Entornos separados para desarrollo y producción.
- Testeos básicos de autenticación y usuarios.
- Integración multilenguaje (i18n) en backend.
