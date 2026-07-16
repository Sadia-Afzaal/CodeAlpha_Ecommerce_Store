# Aurora — E-commerce Store

A complete online store built with Django and SQLite. No React, no build tools, no npm — just clone, run a few commands, and you have a working shop on your machine.

![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/DB-SQLite-003B57?logo=sqlite&logoColor=white)

---

## ✨ Features

**Storefront**
- Fully responsive design that works on all devices
- Hero section, category strips, product grids with hover effects
- Toast notifications and sticky glass navbar

**Product Catalogue**
- Browse by categories
- Search products
- Sort by price, newest, or name
- Pagination, sale badges, star ratings, stock indicators

**Product Detail Pages**
- Product image and description
- Quantity selector
- Related products
- Customer reviews with star ratings

**Shopping Cart**
- AJAX add-to-cart (no page reload)
- Live cart badge updates
- Change quantities or remove items
- Automatic stock limits
- Shows subtotal, shipping, tax, and total

**Checkout & Orders**
- Multi-step checkout process
- Orders wrapped in database transactions
- Automatic stock reduction
- Confirmation page with order reference number

**User Accounts**
- Registration and login/logout
- Profile with saved shipping address
- Address auto-fills at checkout
- Complete order history

**Reviews**
- Logged-in users can rate and comment on products

**Admin Dashboard**
- Manage products, categories, and orders
- View order items inline
- Manage reviews

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 5 (Python) |
| Database | SQLite |
| Frontend | Django templates, custom CSS, vanilla JS |
| Static Files | WhiteNoise |

**Project Structure:**

```
config/     Settings and main URLs
store/      Categories, products, reviews, store views
cart/       Shopping cart logic
orders/     Orders and checkout
accounts/   Registration, login, profiles
templates/  All HTML templates
static/     CSS and JavaScript files
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10, 3.11, or 3.12 installed

### Step 1: Download the Code

**Option A - Clone with Git:**
```bash
git clone https://github.com/Sadia-Afzaal/aurora-ecommerce-store.git
cd aurora-ecommerce-store
```

**Option B - Download ZIP:**
1. Click the green "Code" button
2. Select "Download ZIP"
3. Extract and open the folder

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
```

**Mac/Linux:**
```bash
python3 -m venv .venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Setup Database

```bash
python manage.py migrate
```

### Step 6: Load Demo Data

```bash
python manage.py seed_data
```

This creates sample products, categories, users, and reviews.

### Step 7: Start the Server

```bash
python manage.py runserver
```

### Step 8: Open Your Store

Go to: **http://127.0.0.1:8000/**

---

## 🔐 Demo Accounts

After running `seed_data`, you can login with:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin12345` |
| Customer | `demo` | `demo12345` |

**Admin Panel:** http://127.0.0.1:8000/admin/

---

## 🔄 Reset Demo Data

Want to start fresh?

```bash
python manage.py seed_data --flush
```

This removes all existing data and loads new sample data.

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## ⚙️ Configuration

For production, you can override settings using environment variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`

Check `.env.example` for guidance.

---

## 📝 Notes

**Product Images**
- Products use remote image URLs (`Product.image_url`) to keep the repository small
- You can also upload actual image files through the admin panel
- Uploaded images take priority over URLs

**Payment**
- The checkout "payment" step is a demonstration
- No real payment gateway is connected
- Orders are placed immediately upon submission

---

## ⚠️ Common Issues

| Problem | Solution |
|---------|----------|
| Django not found | Activate virtual environment first |
| Python 3.14 errors | Use Python 3.12 instead |
| Port 8000 in use | Run `python manage.py runserver 8001` |
| "seed_data" not found | Make sure you're in the project folder |

---

## 📄 License

This project is open source and available under the MIT License.

---

Happy Shopping! 🛒
