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

# Django E-Commerce - Vollständiger Shop

## ✨ Features

### Implementiert ✅
- **Produktkatalog** mit Sortierung & Kategorie-Filter
- **Session-basierter Warenkorb** (Gast + User)
- **User Authentication** (Login/Register/Logout)
- **Checkout-System** mit Stock-Verwaltung
- **Bestellübersicht** für eingeloggte User
- **User Dashboard** mit Profilbearbeitung & Adresse
- **Produkt-Kategorien** mit Filterung
- **Dark/Light Mode** Toggle (Catppuccin Latte/Mocha)
- **Responsive Design** (Mobile, Tablet, Desktop)
- **Message System** für User-Feedback
- **Auto-Cart-Merge** nach Login
- **Stock-Checking** beim Checkout
- **Transaction-Safe** Order Creation

### Design
- **Catppuccin Latte** Color Scheme
- **Apple-inspiriertes** minimalistisches Design
- **Fully Responsive** (Mobile, Tablet, Desktop)
- **Custom Fonts** (Clash Display + Epilogue)
- **Smooth Transitions** & Hover Effects
- **Semantic HTML**

## 🚀 Quick Start

### Mit Docker (Empfohlen)

```bash
# Container starten
docker-compose up --build

# In neuem Terminal: Superuser erstellen
docker-compose exec web python manage.py createsuperuser

# Zugriff
Shop: http://localhost:8000
Admin: http://localhost:8000/admin
```

### Ohne Docker

```bash
# Virtuelle Umgebung
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Datenbank & Migrations
python manage.py migrate

# Superuser
python manage.py createsuperuser

# Server starten
python manage.py runserver
```

## 📁 Projektstruktur

```
ecommerce_project/
├── config/
│   └── settings/
│       ├── base.py          # Basis-Settings
│       ├── dev.py           # Development
│       └── prod.py          # Production
├── shop/
│   ├── models.py            # Product, Order, OrderItem, CartItem
│   ├── views.py             # Alle Views (18 Views)
│   ├── cart.py              # Hybrid Cart-Klasse
│   ├── urls.py              # URL-Routing
│   ├── admin.py             # Admin-Konfiguration
│   ├── context_processors.py
│   ├── templates/
│   │   ├── shop/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── products.html
│   │   │   ├── product_detail.html
│   │   │   ├── cart.html
│   │   │   ├── checkout.html
│   │   │   ├── orders.html
│   │   │   ├── order_detail.html
│   │   │   ├── profile.html
│   │   │   ├── header.html
│   │   │   └── footer.html
│   │   └── registration/
│   │       ├── login.html
│   │       └── registration.html
│   └── static/
│       └── css/
│           └── base.css     # Vollständiges Styling
├── media/                   # User-Uploads
├── db/                      # SQLite DB
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env
```

## 🎯 Implementierte Views

| View | URL | Auth | Beschreibung |
|------|-----|------|--------------|
| `home` | `/` | ❌ | Startseite mit Features |
| `products` | `/products/` | ❌ | Produktkatalog + Sortierung |
| `product_detail` | `/products/<id>/` | ❌ | Produktdetails |
| `cart_view` | `/cart/` | ❌ | Warenkorb anzeigen |
| `add_to_cart` | `/cart/add/<id>/` | ❌ | Produkt hinzufügen |
| `remove_from_cart` | `/cart/remove/<id>/` | ❌ | Produkt entfernen |
| `update_cart` | `/cart/update/<id>/` | ❌ | Menge ändern |
| `checkout` | `/checkout/` | ✅ | Bestellung abschließen |
| `orders` | `/orders/` | ✅ | Bestellübersicht |
| `order_detail` | `/orders/<id>/` | ✅ | Einzelne Bestellung |
| `profile` | `/profile/` | ✅ | User-Dashboard |
| `register` | `/register/` | ❌ | Registrierung |
| `login_view` | `/login/` | ❌ | Login + Cart-Merge |
| `logout_view` | `/logout/` | ✅ | Logout |

## 🛠️ Technische Details

### Warenkorb-System

**Hybrid-Ansatz:**
- **Gäste:** Session-basiert (Dictionary)
- **User:** Database-basiert (CartItem Model)
- **Auto-Merge:** Session → DB nach Login

```python
# cart.py
class Cart:
    def __init__(self, request):
        if request.user.is_authenticated:
            # Database Cart
        else:
            # Session Cart
```

### Order-System

**Transaction-Safe:**
```python
with transaction.atomic():
    # Order erstellen
    # OrderItems erstellen
    # Stock reduzieren
    # Cart leeren
```

**Models:**
- `Order`: Header-Daten (User, Total, Status)
- `OrderItem`: Line Items (Product, Quantity, Price)

### Stock-Management

- Stock-Check beim Add-to-Cart
- Stock-Check beim Checkout
- Automatische Reduktion bei Order
- "Nur noch X verfügbar" Anzeige

## 🎨 Design-System

### Catppuccin Latte Colors

```css
--lavender: #7287fd  /* Primary */
--sky: #04a5e5       /* Secondary */
--green: #40a02b     /* Success */
--yellow: #df8e1d    /* Warning */
--red: #d20f39       /* Danger */
--base: #eff1f5      /* Background */
--text: #4c4f69      /* Text */
```

### Typography
- **Headings:** Clash Display (700)
- **Body:** Epilogue (400-600)

### Spacing
- XS: 0.25rem
- SM: 0.5rem
- MD: 1rem
- LG: 1.5rem
- XL: 2rem
- 2XL: 3rem
- 3XL: 4rem

## 📝 Admin-Interface

**Zugriff:** `/admin/`

**Features:**
- Produkt-Verwaltung (Name, Preis, Stock, Bild)
- Bestell-Übersicht mit Filtern
- User-Verwaltung
- CartItem-Übersicht

**Admin-Klassen:**
```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'created_at']
    search_fields = ['name', 'description']
```

## 🔐 Authentication Flow

1. **Gast** fügt Produkte zum Warenkorb hinzu (Session)
2. **Login** → `merge_guest_cart()` wird ausgeführt
3. Session-Cart → Database-Cart übertragen
4. Session-Cart geleert
5. User hat jetzt alle Items in DB

## 📦 Checkout-Flow

1. User klickt "Zur Kasse"
2. Login-Check (Redirect zu Login falls nötig)
3. Checkout-Page mit Bestellübersicht
4. "Jetzt kaufen" → POST-Request
5. Transaction:
   - Order erstellen
   - OrderItems erstellen
   - Stock reduzieren
   - Cart leeren
6. Redirect zu Order-Detail mit Success-Message

## 🚧 Nächste Schritte (Optional)

### Nice-to-Have
- [ ] Produktkategorien
- [ ] Pagination (mehr als 50 Produkte)
- [ ] Produktbewertungen
- [ ] Wishlist
- [ ] Produktsuche (Ajax)
- [ ] Email-Benachrichtigungen
- [ ] Password-Reset
- [ ] Adressverwaltung

### Production-Ready
- [ ] Zahlungsintegration (Stripe/PayPal)
- [ ] PostgreSQL statt SQLite
- [ ] Redis für Sessions
- [ ] Gunicorn + Nginx
- [ ] SSL/HTTPS
- [ ] Email-Backend (SendGrid)
- [ ] Logging & Monitoring
- [ ] Backup-Strategy

## 🧪 Testing

```bash
# Testdaten erstellen (im Admin)
- 10-15 Produkte anlegen
- Verschiedene Preise (10€ - 200€)
- Stock: 0-50 Stück
- Bilder optional

# Test-Szenarios
1. Gast: Produkt → Cart → Login → Checkout → Order
2. User: Produkt → Cart → Checkout → Order anzeigen
3. Leer: Cart leer → "Jetzt einkaufen"
4. Stock: Ausverkauft → "Nicht verfügbar"
5. Profile: Username/Email ändern
```

## 🐛 Debugging

```bash
# Logs ansehen (Docker)
docker-compose logs -f web

# Django Shell
docker-compose exec web python manage.py shell

# Migrations zurücksetzen
docker-compose exec web python manage.py migrate shop zero
docker-compose exec web python manage.py migrate

# Neue Migration
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## 📊 Datenbank-Schema

```sql
-- Product
id, name, description, price, stock, image, created_at

-- Order
id, user_id, total_price, status, created_at

-- OrderItem
id, order_id, product_id, quantity, price

-- CartItem (nur für eingeloggte User)
id, user_id, product_id, quantity
```

## 💡 Architektur-Entscheidungen

### Warum Session-Cart für Gäste?
- Keine Registrierung nötig
- Schneller (kein DB-Schreiben)
- Auto-Cleanup (Session läuft ab)

### Warum DB-Cart für User?
- Multi-Device Support
- Persistent
- Analytics möglich

### Warum Order/OrderItem Split?
- Normalisierung (3NF)
- Historisierung (Preis zum Zeitpunkt)
- Mehrere Produkte pro Order
- Flexible Erweiterungen

### Warum SQLite?
- Ausreichend für Prototyp
- Kein Setup nötig
- Einfache Migration zu PostgreSQL

## 🎓 Lern-Ressourcen

**Django Docs:**
- Models: https://docs.djangoproject.com/en/5.0/topics/db/models/
- Views: https://docs.djangoproject.com/en/5.0/topics/http/views/
- Templates: https://docs.djangoproject.com/en/5.0/topics/templates/

**Catppuccin:**
- Theme: https://github.com/catppuccin/catppuccin

## 👨‍💻 Entwickler

**Lukas Schaffrath**  
Django E-Commerce Prototyp 2025

---

## 📄 Lizenz

Dieses Projekt ist ein Prototyp für Lern- und Demonstrationszwecke.

## 🙏 Credits

- **Django** - Web Framework
- **Catppuccin** - Color Scheme
- **Google Fonts** - Clash Display & Epilogue
