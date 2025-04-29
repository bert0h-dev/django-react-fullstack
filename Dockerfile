# Imagen base
FROM python:3.12-slim

# Evita archivos pyc y salida bufferizada
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el backend completo al contenedor
COPY backend/ /app/

# Exponer el puerto de Django
EXPOSE 8000

# Comando default (se puede sobreescribir en docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]