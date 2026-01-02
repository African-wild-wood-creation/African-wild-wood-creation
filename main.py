from flask import Flask, render_template
from extensions import db
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db" # initialise sql alchemy databse path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from models import ProductCategories, Products

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/contact")
def contact():
    return render_template("Contact.html")

@app.route("/products")
def products():
    product_categories = ProductCategories.query.all()
    return render_template("products.html", categories=product_categories)

@app.route("/products-temp")
def products_temp():
    return render_template("test.html")

@app.route("/order")
def order():
    return render_template("order.html")
    
if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true": # creates database only in the main program
        with app.app_context():
            db.create_all()
            categories = ["tables", "clocks", "mirrors", "lights", "shelves", "coat hangers", "support legs", "signs", "trays", "wine racks", "wood"]
            for category in categories:
                db.session.add(ProductCategories(name=category, img_url=f"{category}_category.png"))
            db.session.commit() # creates databse
    app.run(debug=True)
