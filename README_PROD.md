# 🏭 Pasos para Desplegar en Producción

Este documento resume todo lo necesario para correr el sistema en **modo producción con Docker y Gunicorn**.

---

## ✅ Requisitos

- Docker y docker-compose instalados
- Archivo `.env` con las variables necesarias
- Puerto 5000 y 5432 disponibles en el servidor
- gunicorn agregado en `requirements.txt`

---

## 🗂️ Estructura de archivos clave

sistema_transportes/
├── main.py # Contiene app = create_app()
├── wsgi.py # Expone la app como "application"
├── Dockerfile
├── docker-compose.prod.yml
├── .env
├── requirements.txt


---

## 🚀 Comandos para producción

### 1. Construir y levantar en modo producción:

```bash
docker-compose -f docker-compose.prod.yml up --build -d

2. Ver los logs de la app:

docker-compose -f docker-compose.prod.yml logs -f

3. Apagar los servicios:

docker-compose -f docker-compose.prod.yml down

🧠 Notas importantes

    El archivo wsgi.py debe tener:

from main import app
application = app

    En main.py, al final debe existir:

app = create_app()

    El contenedor web usa Gunicorn para servir la app Flask.

    No se monta el volumen .:/app para evitar conflictos en producción.

🧪 Para probar localmente en modo prod:

docker-compose -f docker-compose.prod.yml up --build

🛠 Mantenimiento

Si agregas nuevas dependencias:

# Actualiza la imagen
docker-compose -f docker-compose.prod.yml build