# 🚚 Sistema Transportes

Sistema de gestión ERP para transportes, desarrollado con **Flask**, **PostgreSQL** y **Docker**.

---

## 📦 Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.10+ (solo si usas entorno virtual para pruebas fuera de Docker)

---

## 🚀 Instalación y ejecución rápida

1. Clona este repositorio:

```bash
git clone https://github.com/ggazuln/Artisa.git
cd sistema_transportes

    ⚠️ Si al clonar la carpeta se llama Artisa, puedes renombrarla a sistema_transportes o ajustar los comandos según corresponda.

⚙️ Configuración del entorno

    Copia el archivo de entorno:

cp .env.example .env

    Edita .env y reemplaza los valores de ejemplo por tus credenciales reales.

🐳 Levantar el entorno con Docker

docker-compose up --build

🔁 En el futuro, si no cambiaste dependencias:

docker-compose up

🕹️ Para ejecutar en segundo plano:

docker-compose up -d

🚫 Para detener:

docker-compose down

🧱 Inicializar la Base de Datos

Una vez los contenedores estén corriendo, ejecuta:

docker-compose exec web flask db upgrade

Esto aplica las migraciones de SQLAlchemy y deja la base de datos lista para operar.
🌐 Acceso a la aplicación

Abre tu navegador y visita:

    http://localhost:5000