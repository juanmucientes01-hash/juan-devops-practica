# Imagen base
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY src/ ./src/

# Crear un usuario sin privilegios y darle permisos sobre el código
RUN useradd appuser && chown -R appuser /app
USER appuser

# Carpeta donde está main.py y puerto por defecto
WORKDIR /app/src
ENV PORT=8000
EXPOSE 8000

# Comando de inicio: servidor uvicorn con la API de FastAPI
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
