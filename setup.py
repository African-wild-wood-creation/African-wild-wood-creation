## Code to seed the databse ##

from main import app
from extensions import db
from models import Products, ProductCategories

with app.app_context():
    db.drop_all()
    db.create_all()

    # ---- create categories ----
    categories = [
        "tables", "clocks", "mirrors", "lights", "shelves",
        "coat hangers", "support legs", "signs", "trays",
        "wine racks", "woods"
    ]

    category_map = {}

    for name in categories:
        cat = ProductCategories(
            name=name,
            img_url=f"{name}_category.png",
            slug=name.replace(" ", "-").lower()
        )
        db.session.add(cat)
        category_map[name] = cat

    db.session.commit()

    PRODUCT_TO_CATEGORY = {
        "table": "tables",
        "clock": "clocks",
        "light": "lights",
        "mirror": "mirrors",
        "shelf": "shelves",
        "tray": "trays",
        "wine rack": "wine racks",
    }

    # ---- create products  ----
    products = {
        "table": 9,
        "clock": 6,
        "light": 2,
        "mirror": 2,
        "shelf": 1,
        "tray": 2,
        "wine rack": 1
    }

    for product_name, count in products.items():
        category_name = PRODUCT_TO_CATEGORY[product_name]
        category = category_map[category_name]

        for i in range(count):
            product = Products(
                name=product_name, 
                img_url=f"{product_name}_{i+1}.png",
                price=0.0,
                category=category
            )
            db.session.add(product)

    db.session.commit()

    print("Database seeded successfully")
