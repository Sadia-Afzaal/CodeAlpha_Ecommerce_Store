# Aurora — Modern E-commerce Store

A polished, full-featured e-commerce web app built with **Django + SQLite** and a
hand-crafted **HTML / CSS / vanilla JS** storefront. No heavy build tooling, no
npm install — clone, run two commands, and you have a professional store running
locally.

![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/DB-SQLite-003B57?logo=sqlite&logoColor=white)

## ✨ Features

- **Modern storefront** — responsive design, hero, category strips, product grids,
  hover animations, toasts, and a sticky glass navbar. Fully mobile-friendly.
- **Product catalogue** — categories, search, sorting (price / newest / name),
  pagination, sale badges, star ratings and stock indicators.
- **Product detail pages** — image, description, quantity selector, related
  products, and customer reviews.
- **Shopping cart** — session-based, add / update / remove, AJAX add-to-cart with
  live cart badge, automatic stock caps, subtotal / shipping / tax / total.
- **Checkout & order processing** — multi-section checkout, order creation inside a
  DB transaction, stock decrement, and a confirmation page with an order reference.
- **User accounts** — registration, login / logout, profile with saved shipping
  address (auto-filled at checkout) and full order history.
- **Reviews** — logged-in users can leave a star rating + comment per product.
- **Admin dashboard** — Django admin for managing products, categories, orders
  (with inline items) and reviews.

## 🧱 Tech stack & architecture

| Layer     | Choice                                        |
|-----------|-----------------------------------------------|
| Backend   | Django 5 (Python)                             |
| Database  | SQLite (zero-config, file-based)              |
| Frontend  | Django templates, custom CSS, vanilla JS      |
| Static    | WhiteNoise (compressed static serving)        |

Apps are split by responsibility:

```
config/    project settings & root URLs
store/     catalogue: Category, Product, Review + storefront views
cart/      session-based Cart class, add/remove/update, context processor
orders/    Order & OrderItem models, checkout & order processing
accounts/  registration, login, Profile (address), order history
templates/ base layout + per-app templates
static/    css/style.css (design system) + js/main.js
```

## 🚀 Getting started

Requires Python 3.10+.

```bash
# 1. (optional) create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 2. install dependencies (lightweight — Django, Pillow, WhiteNoise)
pip install -r requirements.txt

# 3. set up the database and seed demo data
python manage.py migrate
python manage.py seed_data        # products, categories, users, reviews

# 4. run it
python manage.py runserver
```

Then open **http://127.0.0.1:8000/**.

### Demo accounts (created by `seed_data`)

| Role      | Username | Password      |
|-----------|----------|---------------|
| Admin     | `admin`  | `admin12345`  |
| Customer  | `demo`   | `demo12345`   |

Admin dashboard: **http://127.0.0.1:8000/admin/**

> Re-seed from scratch any time with `python manage.py seed_data --flush`.

## 🧪 Tests

```bash
python manage.py test
```

22 tests cover product model logic, storefront views/search, the cart (totals,
stock caps, shipping thresholds), the full checkout flow, and account
registration.

## ⚙️ Configuration

All settings have safe development defaults and can be overridden with env vars
(see `.env.example`): `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`,
`DJANGO_CSRF_TRUSTED_ORIGINS`.

## 📝 Notes

- Product images use curated remote URLs (`Product.image_url`) so the repo stays
  tiny — you can also upload real image files via the admin, which take priority.
- The checkout "payment" step is a demo (no real payment gateway) — orders are
  placed instantly on submit, which is ideal for a portfolio / internship project.
