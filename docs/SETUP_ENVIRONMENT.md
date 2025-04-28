# SETUP\_ENVIRONMENT.md

Guía oficial para configurar y levantar el entorno de desarrollo de este proyecto.

## 🌐 Requisitos Previos

- Python 3.11+
- PostgreSQL 14+
- Docker (opcional, recomendado)
- Docker Compose (opcional, recomendado)
- Git

## 🔢 Clonar el repositorio

```bash
git clone https://github.com/bert0h-dev/tu-repo.git
cd tu-repo
```

## 🔹 Variables de entorno

Debes crear un archivo `.env` en la raíz del proyecto basado en `.env.example`:

```bash
cp .env.example .env
```

**Variables importantes a configurar:**

| Variable                 | Descripción                                   |
| ------------------------ | --------------------------------------------- |
| `DJANGO_SECRET_KEY`      | Llave secreta de Django                       |
| `DJANGO_SETTINGS_MODULE` | Configuración de entorno                      |
| `POSTGRES_DB`            | Nombre de la base de datos                    |
| `POSTGRES_USER`          | Usuario de la base de datos                   |
| `POSTGRES_PASSWORD`      | Contraseña de la base de datos                |
| `POSTGRES_HOST`          | Host de la base de datos ("localhost" o "db") |
| `POSTGRES_PORT`          | Puerto de PostgreSQL (default 5432)           |

## 🏖️ Opcional: levantar entorno con Docker

```bash
docker-compose up --build
```

Esto levantará:

- PostgreSQL
- Django con Gunicorn (modo dev)

Acceso a la app:

```
http://localhost:8000/
```

Acceso a Swagger (documentación interactiva):

```
http://localhost:8000/api/schema/swagger-ui/
```

## 🔧 Levantar entorno manualmente (sin Docker)

1. Crear entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Realizar migraciones:

```bash
python manage.py migrate
```

4. Crear superusuario:

```bash
python manage.py createsuperuser
```

5. Correr el servidor:

```bash
python manage.py runserver
```

Acceder a la app en:

```
http://localhost:8000/
```

## 📊 Estructura de Configuración

| Configuración        | Path                                      |
| -------------------- | ----------------------------------------- |
| Settings base        | `backend/config/settings/base.py`         |
| Settings desarrollo  | `backend/config/settings/development.py`  |
| Settings producción  | `backend/config/settings/production.py`   |
| Dockerfile           | `Dockerfile`                              |
| Docker Compose       | `docker-compose.yml`                      |
| Variables de entorno | `.env` (basado en `.env.example`)         |

## 🚀 Tips adicionales

- Siempre asegúrate de que la variable `DJANGO_SETTINGS_MODULE` esté configurada correctamente.
- Usa Docker para ambientes consistentes y más rápido despliegue.
- Ejecuta `make help` para ver todos los comandos disponibles del proyecto.

## 🔹 Fin del documento
