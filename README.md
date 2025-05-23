# 🚀 Proyecto Backend API - Sistema de Autenticación y Auditoría

Bienvenido a este proyecto backend profesional desarrollado en **Django REST Framework**.  
Aquí aplicamos **arquitectura limpia, control de versiones profesional** y una **gestión pro de cambios** siguiendo los mejores estándares de la industria. 💻🔥

## 🧩 Estructura General

- **Backend:** Django 4.x + Django REST Framework
- **Documentación API:** DRF Spectacular (Swagger UI)
- **Base de Datos:** PostgreSQL

## 🛢️ Gestión de traducciones (i18n)

Este proyecto soporta internacionalización usando **gettext_lazy** y los flujos de mensajes `.po/.mo` de Django.

### Flujo para generar archivos de traducciones

```bash
# Desde la carpeta donde está manage.py

# 1. Crear/actualizar archivos .po para un idioma, por ejemplo español
python manage.py makemessages -l es

# 2. Editar el archivo .po generado en accounts/locale/es/LC_MESSAGES/django.po

# 3. Compilar los archivos de traducción a .mo
python manage.py compilemessages
```

> **Importante:** Asegúrate de tener locales creados en cada app que requiera traducción:
>
> ```bash
> accounts/locale/es/LC_MESSAGES/django.po
> ```

### Comandos útiles de i18n

| Acción | Comando |
|:-------|:--------|
| Crear archivos de traducción | `python manage.py makemessages -l es` |
| Compilar archivos de traducción | `python manage.py compilemessages` |

## 🛂 Estructura del Proyecto

```plaintext
fullproject
├── backend/
│   ├── accounts/
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   ├── s_authentication.py
│   │   │   ├── s_permissions.py
│   │   │   ├── s_roles.py
│   │   │   └── s_users.py
│   │   ├── test/
│   │   │   ├── __init__.py
│   │   │   ├── t_authentication.py
│   │   │   ├── t_change_password.py
│   │   │   ├── t_roles_assign.py
│   │   │   ├── t_roles.py
│   │   │   ├── t_token_refresh.py
│   │   │   └── t_users.py
│   │   ├── urls/
│   │   │   ├── __init__.py
│   │   │   ├── u_assign_user.py
│   │   │   ├── u_authentication.py
│   │   │   ├── u_roles.py
│   │   │   └── u_users.py
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── v_authentication.py
│   │   │   ├── v_permissions.py
│   │   │   ├── v_roles.py
│   │   │   └── v_users.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── filters.py
│   │   ├── models.py
│   │   ├── signals.py
│   │   └── tests.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── accounts/
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── language_from_user.py
│   │   │   ├── thread_user.py
│   │   │   └── update_user_info.py
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   └── s_logs.py
│   │   ├── test/
│   │   │   └── __init__.py
│   │   ├── urls/
│   │   │   ├── __init__.py
│   │   │   └── u_logs.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── logs.py
│   │   │   ├── mixins.py
│   │   │   └── models.py
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   └── v_logs.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── decorators.py
│   │   ├── exceptions.py
│   │   ├── filters.py
│   │   ├── messages.py
│   │   ├── permissions.py
│   │   ├── responses.py
│   │   ├── signals.py
│   │   └── tests.py
│   ├── locale/
│   │   ├── en/
│   │   │   └── LC_MESSAGES/
│   │   │       └── django.po
│   │   └── es/
│   │       └── LC_MESSAGES/
│   │           └── django.po
│   ├── media/
│   ├── static/
│   ├── .env.example
│   ├── manage.py
│   └── requirements.py
├── docs/
├── .config.gitmoji.json
├── .gitignore
├── CHANGELOG.md
├── LICENSE
└── README.md
```

- `backend/accounts/`: Gestión de usuarios, roles, permisos.
- `backend/app/`: Proyecto principal Django.
- `backend/core/`: Gestion de utilerias y bases del proyecto.
- `backend/locale/`: Gestion del idiomas.
- `backend/.env.example`: Variables de entorno de ejemplo.
- `docs/`: Documentación general (changelog, readme).

## ✨ Características principales

- Autenticación segura con JWT.
- Sistema de usuarios, roles (grupos) y permisos.
- Auditoría de accesos y acciones de usuarios.
- Asignación de permisos directos y roles a usuarios.
- Gestión de roles CRUD.
- Swagger UI para la documentación automática de APIs.
- Control de cambios profesional en `CHANGELOG.md`.

## 🛠️ Instalación y configuración rápida

```bash
# Clonar el repositorio
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio

# Crear entorno virtual
python -m venv venv
source venv/bin/activate   # o venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (.env)
# DB, SECRET_KEY, DEBUG, etc.

# Migrar base de datos
python manage.py migrate

# Correr servidor
python manage.py runserver
```

## ⚡ Flujo de trabajo Git profesional

El proyecto sigue un **flujo de ramas pro** basado en Git Flow adaptado:

| Rama | Descripción |
|:-----|:------------|
| `main` | Código estable en producción |
| `develop` | Integración de nuevas funcionalidades *(temporal en versiones previas)* |
| `feature/{nombre}` | Nuevas funcionalidades (base: develop o main) |
| `bugfix/{nombre}` | Correcciones de bugs (base: develop) |
| `release/{version}` | Preparación de nuevas versiones estables |
| `hotfix/{nombre}` | Parches críticos en producción |

## 📦 Cambios y versionado

Este proyecto sigue el principio de **[Keep a Changelog](https://keepachangelog.com/en/1.0.0/)**  
y utiliza **[SemVer](https://semver.org/)** para el versionado.

Consulta todos los cambios en el archivo:

- 📄 [`CHANGELOG.md`](./CHANGELOG.md)

## 🚀 Cómo hacer un Merge Profesional (develop → main)

```bash
git checkout develop
git pull origin develop

git checkout main
git pull origin main

git merge develop
git push origin main

# (Opcional) Eliminar rama develop
git branch -d develop
git push origin --delete develop
```

## 📋 Convenciones de commits

Este proyecto sigue una convención de mensajes de commit para mantener un historial claro:

| Tipo | Descripción |
|:-----|:------------|
| `feat:` | Nuevas funcionalidades |
| `fix:` | Corrección de bugs |
| `docs:` | Cambios en la documentación |
| `refactor:` | Refactorizaciones sin cambios de funcionalidad |
| `test:` | Agregar o corregir tests |
| `chore:` | Tareas menores (actualización de dependencias, scripts) |

Ejemplo:

```bash
git commit -m "feat: implementar CRUD de roles"
```

## 📄 Licencia

Este proyecto es privado y de uso interno.  
Todos los derechos reservados © 2024 [bert0h-dev].

## 🚀 ¡Hecho con pasión! 🔥
