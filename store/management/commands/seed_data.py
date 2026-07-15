import random
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from store.models import Category, Product, Review

U = "https://images.unsplash.com/"
IMG = "?auto=format&fit=crop&w=800&q=80"

CATEGORIES = [
    ("Audio", "🎧", "Headphones, speakers and everything sound."),
    ("Wearables", "⌚", "Smart watches and fitness trackers."),
    ("Home", "🏠", "Design-led objects for modern living."),
    ("Workspace", "🖥️", "Gear that makes work feel effortless."),
    ("Accessories", "🎒", "The finishing touches that matter."),
    ("Lifestyle", "🌿", "Wellness and everyday carry."),
]

# (category, name, brand, tagline, price, compare_at, stock, featured, image, description)
PRODUCTS = [
    ("Audio", "Studio Wireless Headphones", "Auralux", "Reference sound, all-day comfort",
     249.00, 329.00, 24, True, "photo-1505740420928-5e560c06d30e",
     "Immersive 40mm drivers, adaptive noise cancellation and 40-hour battery life. Memory-foam ear cushions and a featherweight frame make these disappear on your head."),
    ("Audio", "Pebble True Wireless Earbuds", "Auralux", "Tiny buds, huge sound",
     129.00, None, 60, True, "photo-1590658268037-6bf12165a8df",
     "Crystal-clear calls, IPX5 sweat resistance and a pocketable charging case. Six hours per charge, 30 with the case."),
    ("Audio", "Orbit Portable Speaker", "Sonora", "Room-filling 360° audio",
     89.00, 119.00, 40, False, "photo-1608043152269-423dbba4e7e1",
     "A palm-sized speaker with surprising low-end. Waterproof, dustproof and built for the beach, the shower or the backyard."),
    ("Audio", "Maestro Turntable", "Sonora", "Analog warmth, modern build",
     299.00, None, 12, False, "photo-1461360370896-922624d12aa1",
     "Belt-driven precision with a built-in preamp and Bluetooth out. Spin your vinyl or stream it — no receiver required."),

    ("Wearables", "Pulse Smartwatch Series 5", "Nimbus", "Your health, on your wrist",
     279.00, 349.00, 30, True, "photo-1523275335684-37898b6baf30",
     "A vivid always-on AMOLED display, ECG, SpO2 and 7-day battery. Tracks 120+ workouts and syncs with everything."),
    ("Wearables", "Trek Fitness Band", "Nimbus", "Lightweight everyday tracking",
     69.00, 89.00, 80, False, "photo-1575311373937-040b8e1fd5b6",
     "Slim, water-resistant and always ready. Steps, sleep, heart-rate and 14-day battery in a band you'll forget you're wearing."),
    ("Wearables", "Vista AR Glasses", "Nimbus", "Notifications, hands-free",
     399.00, None, 8, False, "photo-1625480860249-be231d5b3aa5",
     "Discreet heads-up notifications and turn-by-turn directions in a classic frame. All-day comfort, prescription-ready."),

    ("Home", "Lumen Smart Lamp", "Halo", "Light that adapts to you",
     79.00, 99.00, 45, True, "photo-1507473885765-e6ed057f782c",
     "16 million colours, circadian scheduling and voice control. Wake up gently and wind down warm."),
    ("Home", "Terra Ceramic Diffuser", "Halo", "Calm, one mist at a time",
     49.00, None, 55, False, "photo-1602874801007-bd458bb1b8b6",
     "Hand-glazed stoneware with whisper-quiet ultrasonic misting and a soft ambient glow. Runs up to 10 hours."),
    ("Home", "Nimbus Espresso Machine", "Brewhaus", "Café-quality at home",
     449.00, 549.00, 15, True, "photo-1517668808822-9ebb02f2a0e6",
     "15-bar pump, precise PID temperature control and a pro steam wand. Pull rich espresso and micro-foam milk like a barista."),
    ("Home", "Fold Throw Blanket", "Loomly", "Cloud-soft, endlessly cozy",
     59.00, None, 70, False, "photo-1600369672770-985fd30004eb",
     "Chunky knit in OEKO-TEX cotton. The kind of blanket you fight over on the couch."),

    ("Workspace", "Glide Mechanical Keyboard", "Keystone", "Type on a cloud",
     159.00, 199.00, 35, True, "photo-1587829741301-dc798b83add3",
     "Hot-swappable switches, gasket mount and per-key RGB. Wireless or wired, Mac and PC ready."),
    ("Workspace", "Contour Ergonomic Mouse", "Keystone", "Comfort that lasts all day",
     79.00, None, 50, False, "photo-1527864550417-7fd91fc51a46",
     "A sculpted vertical shape that keeps your wrist neutral. Silent clicks, 4000 DPI and USB-C charging."),
    ("Workspace", "Riser Laptop Stand", "Deskly", "Eye-level, everywhere",
     69.00, 89.00, 60, False, "photo-1527864550417-7fd91fc51a46",
     "Aircraft-grade aluminium that folds flat for travel. Raises your screen to a healthier height."),
    ("Workspace", "Beam Desk Webcam 4K", "Keystone", "Look your best on every call",
     129.00, None, 28, False, "photo-1587825140708-dfaf72ae4b04",
     "Sharp 4K sensor, HDR and AI auto-framing. Built-in privacy shutter and dual noise-cancelling mics."),

    ("Accessories", "Voyage Weekender Bag", "Field&Co", "Pack for anything",
     139.00, 179.00, 22, True, "photo-1553062407-98eeb64c6a62",
     "Water-resistant waxed canvas with a padded laptop sleeve and a shoe compartment. Carry-on friendly."),
    ("Accessories", "Nomad Leather Wallet", "Field&Co", "Slim, smart, timeless",
     45.00, None, 90, False, "photo-1627123424574-724758594e93",
     "Full-grain leather that ages beautifully. RFID-blocking and just the right size for cards and cash."),
    ("Accessories", "Anchor 100W USB-C Charger", "Voltix", "Charge everything, fast",
     55.00, 69.00, 65, False, "photo-1583863788434-e58a36330cf0",
     "GaN tech in a tiny brick. Four ports, enough power for a laptop and phone at once."),
    ("Accessories", "Shade Polarized Sunglasses", "Field&Co", "See clearly, look sharp",
     89.00, None, 40, False, "photo-1511499767150-a48a237f0083",
     "Italian acetate frames and polarized lenses that cut glare. Includes a hard case and cleaning cloth."),

    ("Lifestyle", "Hydra Insulated Bottle", "Everspring", "Cold for 24h, hot for 12h",
     35.00, 45.00, 100, True, "photo-1602143407151-7111542de6e8",
     "Double-wall vacuum steel with a leakproof lid. Fits every cup holder and keeps drinks perfect all day."),
    ("Lifestyle", "Calm Weighted Eye Mask", "Everspring", "Deeper rest, instantly",
     29.00, None, 75, False, "photo-1556228578-8c89e6adf883",
     "Gently weighted, contoured to block all light. Washable silk-touch cover for restorative sleep."),
    ("Lifestyle", "Grove Yoga Mat", "Everspring", "Grip that moves with you",
     69.00, 89.00, 38, False, "photo-1601925260368-ae2f83cf8b7f",
     "Natural rubber with a non-slip top layer and alignment lines. Comes with a carry strap."),
    ("Lifestyle", "Ember Scented Candle", "Halo", "Warm evenings in a jar",
     32.00, None, 85, False, "photo-1602874801007-bd458bb1b8b6",
     "Hand-poured soy wax with notes of amber, cedar and vanilla. 50-hour clean burn."),
]

REVIEW_SNIPPETS = [
    ("Absolutely love this — exceeded my expectations.", 5),
    ("Great quality for the price. Would buy again.", 5),
    ("Solid product, does exactly what it promises.", 4),
    ("Beautiful design and works perfectly.", 5),
    ("Good, but shipping took a little longer than expected.", 4),
    ("Best purchase I've made this year!", 5),
    ("Decent, though I expected slightly better build.", 3),
    ("My favourite thing right now. Highly recommend.", 5),
]


class Command(BaseCommand):
    help = "Seed the database with demo categories, products, users and reviews."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush", action="store_true", help="Delete existing catalogue first."
        )

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(42)

        if options["flush"]:
            Review.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write("Cleared existing catalogue.")

        cat_map = {}
        for name, icon, desc in CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                name=name, defaults={"icon": icon, "description": desc}
            )
            cat.icon = icon
            cat.description = desc
            cat.save()
            cat_map[name] = cat
        self.stdout.write(f"Categories: {len(cat_map)}")

        created = 0
        products = []
        for (
            cat_name, name, brand, tagline, price, compare, stock, featured, photo, desc
        ) in PRODUCTS:
            product, was_created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": cat_map[cat_name],
                    "brand": brand,
                    "tagline": tagline,
                    "description": desc,
                    "price": Decimal(str(price)),
                    "compare_at_price": Decimal(str(compare)) if compare else None,
                    "image_url": f"{U}{photo}{IMG}",
                    "stock": stock,
                    "is_featured": featured,
                },
            )
            if not was_created:
                product.category = cat_map[cat_name]
                product.brand = brand
                product.tagline = tagline
                product.description = desc
                product.price = Decimal(str(price))
                product.compare_at_price = Decimal(str(compare)) if compare else None
                product.image_url = f"{U}{photo}{IMG}"
                product.stock = stock
                product.is_featured = featured
                product.save()
            else:
                created += 1
            products.append(product)
        self.stdout.write(f"Products: {len(products)} ({created} new)")

        # Demo users
        admin, admin_created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@aurora.test", "is_staff": True, "is_superuser": True},
        )
        if admin_created:
            admin.set_password("admin12345")
            admin.save()
            self.stdout.write("Created superuser: admin / admin12345")

        demo, demo_created = User.objects.get_or_create(
            username="demo",
            defaults={"email": "demo@aurora.test", "first_name": "Demo"},
        )
        if demo_created:
            demo.set_password("demo12345")
            demo.save()
            self.stdout.write("Created demo user: demo / demo12345")

        reviewers = []
        for uname in ("alex", "sam", "priya", "jordan", "maria"):
            u, c = User.objects.get_or_create(
                username=uname,
                defaults={"first_name": uname.capitalize(), "email": f"{uname}@aurora.test"},
            )
            if c:
                u.set_password("password123")
                u.save()
            reviewers.append(u)

        review_count = 0
        for product in products:
            for reviewer in random.sample(reviewers, random.randint(1, 4)):
                comment, rating = random.choice(REVIEW_SNIPPETS)
                _, c = Review.objects.get_or_create(
                    product=product,
                    user=reviewer,
                    defaults={"rating": rating, "comment": comment},
                )
                if c:
                    review_count += 1
        self.stdout.write(f"Reviews: {review_count} new")

        self.stdout.write(self.style.SUCCESS("✓ Seed complete."))
