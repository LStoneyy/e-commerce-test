# e-commerce-test
Ein modularer Django-E-Commerce-Prototyp als Aufgabe für Jovoco.

## Quick Start

```bash
# git repo pullen/clonen
git clone https://github.com/LStoneyy/e-commerce-test.git
cd e-commerce-test/

# .env für sensible daten kopieren, dann:
docker-compose -f docker-compose.dev.yml up -d --build

# Superuser erstellen und migrieren
docker exec -it e-commerce-test bash
python manage.py createsuperuser
python manage.py migrate
exit

# Zugriff
Shop: http://localhost:8000 oder http://127.0.0.1:8000/
Admin: http://localhost:8000/admin oder http://127.0.0.1:8000/admin/
```

