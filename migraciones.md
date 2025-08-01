# 🛠️ Migraciones de Base de Datos (Flask-Migrate)

Este proyecto usa **Flask-Migrate + Alembic** para versionar los cambios en los modelos y mantener sincronizada la base de datos.

---

## 🧩 Crear una nueva migración

Siempre que modifiques tus modelos (por ejemplo, agregues columnas o tablas nuevas):

```bash
docker-compose exec web flask db migrate -m "Describe el cambio"
