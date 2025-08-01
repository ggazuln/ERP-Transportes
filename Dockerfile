# Usar una imagen base oficial de Python optimizada
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente al contenedor
COPY . .

# Exponer el puerto 5000 (opcional pero recomendado)
EXPOSE 5000

# Deja que docker-compose defina el comando
