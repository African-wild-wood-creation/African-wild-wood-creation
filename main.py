from flask import Flask, render_template, request, redirect, url_for, session
from extensions import db
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GMAIL_USER = "awwtest6@gmail.com" # the email that will hold the info
GMAIL_APP_PASSWORD = "yhwo fcsr woyj zrpf"  # Gmail app password

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db" # initialise sql alchemy databse path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

def send_email(subject, to_email, html_body):
    msg = MIMEMultipart("alternative")
    msg["From"] = GMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach HTML body
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

db.init_app(app)

from models import ProductCategories, Products

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["nm"]
        phone = request.form["num"]
        email = request.form["email"] # users email
        address = request.form["addr"]
        creation = request.form["creatxt"]
        picnum = request.form["catpicnum"]
        dimensions = request.form["dim"]
        wood = request.form["prefwood"]
        finish = request.form["finish"]
        suggests = request.form["suggests"]

        html_body = f"""
        <h2>New Order Request</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Address:</strong> {address}</p>
        <p><strong>Creation Interested In:</strong> {creation}</p>
        <p><strong>Catalogue Picture Number:</strong> {picnum}</p>
        <p><strong>Dimensions:</strong> {dimensions}</p>
        <p><strong>Preferred Wood:</strong> {wood}</p>
        <p><strong>Preferred Finish:</strong> {finish}</p>
        <p><strong>Suggestions:</strong><br>{suggests}</p>
        """

        send_email(
            subject="New Contact",
            to_email="africanwildwood@gmail.com", # who it will be sent to (kens email)
            html_body=html_body
        )

        return render_template("Contact.html", success=True)

    return render_template("Contact.html")

@app.route("/products")
def products():
    product_categories = ProductCategories.query.all()
    return render_template("products.html", categories=product_categories)

@app.route("/products/<string:category_slug>")
def products_by_category(category_slug):
    category = ProductCategories.query.filter_by(slug=category_slug).first()
    products = category.products
    return render_template("category.html", category=category, products=products)

@app.route("/products-temp")
def products_temp():
    return render_template("test.html")

@app.route("/order", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        name = request.form["nm"]
        phone = request.form["num"]
        email = request.form["email"] # users email
        address = request.form["addr"]
        creation = request.form["creatxt"]
        picnum = request.form["catpicnum"]
        dimensions = request.form["dim"]
        wood = request.form["prefwood"]
        finish = request.form["finish"]
        suggests = request.form["suggests"]

        html_body = f"""
        <h2>New Order Request</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Address:</strong> {address}</p>
        <p><strong>Creation Interested In:</strong> {creation}</p>
        <p><strong>Catalogue Picture Number:</strong> {picnum}</p>
        <p><strong>Dimensions:</strong> {dimensions}</p>
        <p><strong>Preferred Wood:</strong> {wood}</p>
        <p><strong>Preferred Finish:</strong> {finish}</p>
        <p><strong>Suggestions:</strong><br>{suggests}</p>
        """

        send_email(
            subject="New Order Request",
            to_email="africanwildwood@gmail.com", # who it will be sent to (kens email)
            html_body=html_body
        )

        return render_template("order.html", success=True)

    return render_template("order.html")

@app.route("/cart")
def cart():
    cart = session.get("cart", [])

    total = sum(item["price"] * item["quantity"] for item in cart)

    return render_template("cart.html", cart=cart, total=total)

@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    product = Products.query.get_or_404(product_id)

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]

    # Check if item already in cart
    for item in cart:
        if item["product_id"] == product.product_id:
            item["quantity"] += 1
            break
    else:
        cart.append({
            "product_id": product.product_id,
            "name": product.name,
            "price": float(product.price),
            "quantity": 1
        })

    session["cart"] = cart
    session.modified = True

    return redirect(request.referrer or url_for("products"))

@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])

    cart = [item for item in cart if item["product_id"] != product_id]

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))


if __name__ == "__main__":           
    app.run(debug=True)
