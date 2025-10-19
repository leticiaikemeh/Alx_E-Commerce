

# E-commerce Product API (Django + DRF)

A clean, deployable backend for managing products on an e-commerce platform. Supports **JWT authentication**, **product & category CRUD**, **search**, **filtering**, **ordering**, and **pagination**. Designed as an ALX Backend capstone but built to production practices.

---

## ✨ Features

* **Auth**: Register + JWT login (access/refresh), `Authorization: Bearer <token>`
* **Products**: Create / Read / Update / Delete
* **Categories**: Create / Read / Update / Delete
* **Search**: Partial match on product name and category name
* **Filtering**: Category (id/slug), price range, in-stock, active
* **Ordering**: by created date, price, name, stock quantity
* **Pagination**: Page-number pagination with default page size = 10
* **Production-ready**: Dockerfile, WhiteNoise, env-driven settings, Postgres support via `DATABASE_URL`

> Stretch hooks included for reviews, multiple images, wishlists, promotions, and safe stock decrement on orders.

---

## 📁 Project Structure

```
Alx_DjangoLearnLab/
└─ ecommerce_api/
   ├─ Dockerfile
   ├─ docker-compose.yml           
   ├─ requirements.txt
   ├─ .env.sample
   ├─ manage.py
   ├─ ecommerce_api/
   │  ├─ settings.py
   │  ├─ urls.py
   │  ├─ wsgi.py
   ├─ accounts/
   │  ├─ serializers.py
   │  ├─ urls.py
   │  ├─ views.py
   ├─ catalog/
   │  ├─ models.py
   │  ├─ serializers.py
   │  ├─ permissions.py
   │  ├─ urls.py
   │  ├─ views.py
   └─ tests/                      
```

---

## 🧰 Tech Stack

* **Python** 3.12+
* **Django** 5.x
* **Django REST Framework**
* **SimpleJWT** for authentication
* **django-filter** for robust filtering
* **PostgreSQL** (prod) / **SQLite** (dev default)
* **WhiteNoise** for static files in production
* **Gunicorn** as WSGI server
* Deploy targets: **Heroku** or **PythonAnywhere**

---

## 🚀 Getting Started (Local)

### 1) Clone & create virtual environment

```bash
git clone https://github.com/<you>/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r ecommerce_api/requirements.txt
```

> If `requirements.txt` is not committed yet, install manually:
> `pip install "django>=5.0" djangorestframework djangorestframework-simplejwt django-filter pillow psycopg[binary] dj-database-url python-dotenv whitenoise gunicorn`

### 3) Environment variables

Copy `.env.sample` to `.env` and adjust as needed:

```env
# .env
DEBUG=True
DJANGO_SECRET_KEY=change-me
ALLOWED_HOSTS=localhost,127.0.0.1
# For local SQLite leave DATABASE_URL unset, or:
# DATABASE_URL=sqlite:///db.sqlite3
```

> In production, set `DEBUG=False`, provide a strong `DJANGO_SECRET_KEY`, and set a real `ALLOWED_HOSTS` value.

### 4) Migrate & run

```bash
cd ecommerce_api
python manage.py migrate
python manage.py createsuperuser  # optional for admin site
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`.

---

## 🔐 Authentication

* **Register**: `POST /api/accounts/register/`
* **Login (JWT)**: `POST /api/auth/login/` → returns `{access, refresh}`
* **Refresh**: `POST /api/auth/refresh/`
* **Current user**: `GET/PATCH /api/accounts/me/` (requires `Authorization: Bearer <access>`)

🔐 Register

**Example**

```http
POST /api/accounts/register/
Content-Type: application/json

{
  "username": "myk",
  "email": "myk@example.com",
  "password": "pass12345"
}
```

**Responses**

201 Created
```json
{
  "id": 7,
  "username": "myk",
  "email": "myk@example.com",
  "is_staff": false
}
```

400 Bad Request (examples)
```json
{ "password": ["Ensure this field has at least 8 characters."] }
```
```json
{ "username": ["A user with that username already exists."] }
```

🔐 Login

**Example**
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "myk",
  "password": "pass12345"
}
```

**Response**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```

Use the access token:

```
Authorization: Bearer <access>
```

---

## 📦 Domain Model

### Category

* `id`, `name` (unique), `slug` (unique), `created_at`

### Product

* `id`, `name`, `description`, `price`, `category` (FK),
  `stock_qty`, `image_url`, `is_active`, `created_at`, `updated_at`

**Validations**

* `name`, `price`, `stock_qty`, `category` required on create
* `price` must be non-negative

---

## 🧭 API Endpoints

Base URL: `/api`

### Accounts

|       Method | Endpoint                |  Auth | Description                   |
| -----------: | ----------------------- | :---: | ----------------------------- |
|         POST | `/accounts/register/`   |   No  | Create a new user             |
|         POST | `/auth/login/`          |   No  | Obtain JWT tokens             |
|         POST | `/auth/refresh/`        |   No  | Refresh access token          |
|          GET | `/accounts/me/`         |  Yes  | Get current user              |
|        PATCH | `/accounts/me/`         |  Yes  | Update current user           |
|          GET | `/accounts/users/`      | Admin | List users (optional)         |
|         POST | `/accounts/users/`      | Admin | Create user (optional)        |
|          GET | `/accounts/users/{id}/` | Admin | Retrieve a user (optional)    |
| PATCH/DELETE | same                    | Admin | Update/Delete user (optional) |

### Categories

|    Method | Endpoint                    | Auth | Notes             |
| --------: | --------------------------- | :--: | ----------------- |
|       GET | `/catalog/categories/`      |  No  | List/search/order |
|      POST | `/catalog/categories/`      |  Yes | Create            |
|       GET | `/catalog/categories/{id}/` |  No  | Retrieve          |
| PUT/PATCH | `/catalog/categories/{id}/` |  Yes | Update            |
|    DELETE | `/catalog/categories/{id}/` |  Yes | Delete            |

### Products

|    Method | Endpoint                  | Auth | Notes                                                          |
| --------: | ------------------------- | :--: | -------------------------------------------------------------- |
|       GET | `/catalog/products/`      |  No  | List with **search**, **filter**, **ordering**, **pagination** |
|      POST | `/catalog/products/`      |  Yes | Create                                                         |
|       GET | `/catalog/products/{id}/` |  No  | Retrieve                                                       |
| PUT/PATCH | `/catalog/products/{id}/` |  Yes | Update                                                         |
|    DELETE | `/catalog/products/{id}/` |  Yes | Delete                                                         |

**Search & Filters**

* **Search**: `?search=<text>` (matches `name` and `category__name`, partial/contains)
* **Filters**:

  * `category=<id>`
  * `category_slug=<slug>`
  * `min_price=<number>`
  * `max_price=<number>`
  * `in_stock=true|false`
  * `is_active=true|false`
* **Ordering**: `?ordering=price` (or `-price`, `name`, `created_at`, `stock_qty`)
* **Pagination**: page number via `?page=2` (default page size 10)

**Examples**

```
GET /api/catalog/products/?search=shirt&category_slug=clothing&min_price=20&max_price=80&in_stock=true&ordering=-price&page=2
```

---

## 📝 Example Requests

### Create Category

```http
POST /api/catalog/categories/
Authorization: Bearer <access>
Content-Type: application/json

{
  "name": "Electronics",
  "slug": "electronics"
}
```

### Create Product

```http
POST /api/catalog/products/
Authorization: Bearer <access>
Content-Type: application/json

{
  "name": "Phone X",
  "description": "Sleek 128GB model",
  "price": "499.99",
  "category": 1,
  "stock_qty": 20,
  "image_url": "https://example.com/img/phonex.jpg",
  "is_active": true
}
```

### List Products (search + filter)

```http
GET /api/catalog/products/?search=phone&min_price=300&in_stock=true&ordering=price
```

### Retrieve Product

```http
GET /api/catalog/products/42/
```

---

## ⚙️ Error Handling (typical responses)

* **400 Bad Request** — validation errors
* **401 Unauthorized** — missing/invalid JWT
* **403 Forbidden** — authenticated but not permitted (if you restrict to staff)
* **404 Not Found** — resource not found

**Example 400**

```json
{
  "price": ["Price cannot be negative."]
}
```

---

## 🧪 Testing

Minimal sample to verify flow (Django test client):

```python
# catalog/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from catalog.models import Category

class ProductFlow(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pass12345")
        token = self.client.post(reverse("jwt_obtain"), {"username":"tester","password":"pass12345"}).data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.cat = Category.objects.create(name="Electronics", slug="electronics")

    def test_create_and_list(self):
        r = self.client.post("/api/catalog/products/", {
            "name":"Phone X","price":"499.99","category": self.cat.id,"stock_qty": 10
        })
        self.assertEqual(r.status_code, 201)
        list_r = self.client.get("/api/catalog/products/?search=phone&min_price=400&in_stock=true")
        self.assertEqual(list_r.status_code, 200)
```

Run tests:

```bash
python manage.py test
```

---

## 🐳 Docker (optional but recommended)

**Dockerfile** (production-ready)

```dockerfile
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "ecommerce_api.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**docker-compose.yml** (for local Postgres dev)

```yaml
version: "3.9"
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: shop
      POSTGRES_PASSWORD: shop
      POSTGRES_DB: shop
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
  web:
    build: .
    env_file: .env
    ports: ["8000:8000"]
    depends_on: [db]
volumes:
  pgdata:
```

**.env.sample**

```
DEBUG=True
DJANGO_SECRET_KEY=change-me
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://shop:shop@db:5432/shop
```

---

## ☁️ Deployment

### Heroku (container deploy)

1. Create Heroku app & add Postgres add-on
2. Configure env vars:

   * `DEBUG=False`
   * `DJANGO_SECRET_KEY=<strong-secret>`
   * `ALLOWED_HOSTS=<yourapp>.herokuapp.com`
   * `DATABASE_URL` is auto-set by add-on
3. Deploy the container (or use buildpacks)
4. Post-deploy:

   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### PythonAnywhere

1. Create a virtualenv and install `requirements.txt`
2. Set WSGI app to `ecommerce_api.wsgi:application`
3. Add env vars in the Web config
4. Run `collectstatic`, `migrate`, `createsuperuser` from the Bash console

**Security checklist (prod):**

* `DEBUG=False`
* Strong `DJANGO_SECRET_KEY`
* Proper `ALLOWED_HOSTS`
* HTTPS enforced at the platform / proxy
* Rotate credentials and use least privilege on DB

---

## 🔄 Future Enhancements (Stretch)

* **Reviews & Ratings**: `Review(product, user, rating 1–5, comment)` + unique `(user, product)`; denormalize average rating
* **Advanced Categories**: full CRUD (already supported), hierarchical categories if needed
* **Multiple Images**: `ProductImage(product, image_url)` + nested read serializer
* **Wishlist**: `Wishlist(user)` + `WishlistItem(wishlist, product)` with unique constraint
* **Stock Management**: safe decrement on order

  ```python
  from django.db import transaction
  with transaction.atomic():
      p = Product.objects.select_for_update().get(pk=product_id)
      if p.stock_qty < qty: raise ValueError("Insufficient stock.")
      p.stock_qty -= qty; p.save()
  ```
* **Promotions**: `Promotion(product/category, percent_off, starts_at, ends_at, active)`, computed `effective_price`

---

## 🔧 Troubleshooting

* **401 Unauthorized**: Ensure you include `Authorization: Bearer <access>`.
* **403 Forbidden**: You’re authenticated but not allowed (if restricted to staff).
* **400 Bad Request**: Check serializer validation messages.
* **CORS**: If you add a frontend, configure `django-cors-headers`.

---

## 📜 License

MIT (or your preferred license).

---

## 🤝 Contributing

PRs welcome. Please:

1. Create a feature branch.
2. Add/adjust tests if needed.
3. Keep code formatted and lint-clean.

---

## 📚 Quick Reference

* Run dev server: `python manage.py runserver`
* Run migrations: `python manage.py makemigrations && python manage.py migrate`
* Create admin: `python manage.py createsuperuser`
* Collect static (prod): `python manage.py collectstatic`
* Tests: `python manage.py test`

---

If you want, I can also generate a Postman collection and a seed script for sample categories/products.
