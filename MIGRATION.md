# Migration Guide - Neue Features

## Übersicht der Änderungen

Diese Updates fügen folgende Features hinzu:
- ✅ UserProfile mit vollständiger Adresse
- ✅ Produkt-Kategorien mit Filterung
- ✅ Dark/Light Mode Toggle
- ✅ Verbesserte Button-Layouts
- ✅ Erweiterte Profile-Verwaltung

## Schritt-für-Schritt Migration

### 1. Backup erstellen (Wichtig!)

```bash
# Docker
docker-compose exec web python manage.py dumpdata > backup.json

# Lokal
python manage.py dumpdata > backup.json
```

### 2. Neue Models-Datei übernehmen

Ersetze `shop/models.py` mit der neuen Version die folgende Models enthält:
- `UserProfile` - Erweiterte User-Daten
- `Category` - Produktkategorien

### 3. Admin-Datei aktualisieren

Ersetze `shop/admin.py` mit der neuen Version.

### 4. Views aktualisieren

Aktualisiere `shop/views.py`:
- Import `Category` hinzufügen
- `products()` View mit Kategorie-Filter
- `profile()` View mit UserProfile

### 5. Templates aktualisieren

Ersetze folgende Templates:
- `shop/templates/shop/header.html` (Theme Toggle)
- `shop/templates/shop/profile.html` (Erweiterte Form)
- `shop/templates/shop/products.html` (Kategorie-Filter)

### 6. CSS & JavaScript

- Ersetze `static/css/base.css`
- Erstelle `static/js/base.js` (Theme Toggle)

### 7. Migrations erstellen & ausführen

```bash
# Docker
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Lokal
python manage.py makemigrations
python manage.py migrate
```

### 8. Testdaten erstellen

```bash
# Admin öffnen
# → Categories erstellen (z.B. "Elektronik", "Kleidung", "Sport")
# → Produkte den Kategorien zuordnen
```

## Beispiel-Kategorien

Im Django Admin unter "Categories":

```
Name: Elektronik
Slug: elektronik
Description: Smartphones, Laptops, Tablets

Name: Kleidung  
Slug: kleidung
Description: T-Shirts, Hosen, Jacken

Name: Sport
Slug: sport
Description: Sportgeräte und Zubehör

Name: Haushalt
Slug: haushalt
Description: Küchengeräte, Deko, Möbel
```

## Troubleshooting

### Problem: Migration-Fehler bei UserProfile

**Lösung:**
```bash
# Alte Migrations löschen (außer __init__.py)
rm shop/migrations/00*.py

# Neu erstellen
python manage.py makemigrations shop
python manage.py migrate shop
```

### Problem: Bestehende User haben kein Profile

**Lösung:**
```python
# Django Shell
python manage.py shell

from django.contrib.auth.models import User
from shop.models import UserProfile

for user in User.objects.all():
    UserProfile.objects.get_or_create(user=user)
```

### Problem: Theme Toggle funktioniert nicht

**Prüfen:**
1. `base.js` in `static/js/` vorhanden?
2. In `base.html`: `<script defer src="{% static '/js/base.js' %}"></script>`
3. Browser-Cache leeren

### Problem: Kategorien werden nicht angezeigt

**Prüfen:**
1. Kategorien im Admin erstellt?
2. `Category` Model in `views.py` importiert?
3. Template `products.html` aktualisiert?

## Nach der Migration testen

### ✅ Checkliste:

- [ ] Theme Toggle (Sonne/Mond-Icon im Header)
- [ ] Dark Mode funktioniert (Farben ändern sich)
- [ ] Theme-Präferenz bleibt nach Reload
- [ ] Kategorie-Filter auf Products-Page
- [ ] Produkte zeigen Kategorie-Badge
- [ ] Profile-Form hat alle Adress-Felder
- [ ] Profile speichert korrekt
- [ ] Bestehende Orders funktionieren noch
- [ ] Warenkorb funktioniert noch
- [ ] Checkout funktioniert noch

## Rollback (Falls nötig)

```bash
# Datenbank-Backup wiederherstellen
python manage.py flush  # ⚠️ Löscht alle Daten!
python manage.py loaddata backup.json

# Alte Dateien zurück (Git)
git checkout HEAD -- shop/models.py shop/views.py
```

## Production Deployment

### Vor dem Deployment:

1. ✅ Alle Tests durchgeführt
2. ✅ Backup erstellt
3. ✅ Static files gesammelt: `python manage.py collectstatic`
4. ✅ Migrations getestet
5. ✅ Theme Toggle in verschiedenen Browsern getestet

### Deployment-Steps:

```bash
# 1. Code deployen
git push production main

# 2. Migrations ausführen
python manage.py migrate

# 3. Static files
python manage.py collectstatic --noinput

# 4. Server neustarten
systemctl restart gunicorn  # oder dein Service
```

## Support

Bei Problemen:
1. Logs prüfen: `docker-compose logs -f web`
2. Django Shell testen: `python manage.py shell`
3. Migrations Status: `python manage.py showmigrations`

---

**Geschätzte Migrations-Zeit:** 10-15 Minuten
**Downtime:** ~2 Minuten (nur während Migrations)
