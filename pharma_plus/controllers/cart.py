from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from pharma_plus import db
from pharma_plus.models.product import Product
from pharma_plus.models.user import User
from pharma_plus.utility.user_cart_manager import Cart
from pharma_plus.utility.user_login_manager import customer_login_required
from pharma_plus.utility.user_session_manager import CurrentUser

cart = Blueprint("cart", __name__)


@cart.route("/add_to_cart/<string:product_id>", methods=["GET"])
@customer_login_required
def add_to_cart(product_id: str):
    if Cart.add_to_cart(product_id):
        flash("Product added to cart", "success")
    return redirect(url_for("products.product", product_id=product_id))


@cart.route("/increase/<string:product_id>", methods=["GET"])
@customer_login_required
def increase(product_id: str):
    if Cart.increase(product_id):
        flash("Cart Updated", "success")
    return redirect(url_for("products.product", product_id=product_id))


@cart.route("/decrease/<string:product_id>", methods=["GET"])
@customer_login_required
def decrease(product_id: str):
    if Cart.decrease(product_id):
        flash("Cart Updated", "success")
    return redirect(url_for("products.product", product_id=product_id))


@cart.route("/cart", methods=["GET"])
@customer_login_required
def show_cart():

    cart = session["cart"]

    products = (
        db.session.query(Product)
        .filter(Product.id.in_([int(k) for k in cart.keys()]))
        .all()
    )

    for product in products:
        product.quantity = cart[str(product.id)]

    out_of_stock_exist = False
    for product in products:
        if int(product.quantity) > product.stock:
            product.out_of_stock = True
            out_of_stock_exist = True

    total_price = sum([product.price * int(product.quantity) for product in products])
    total_products = sum([int(product.quantity) for product in products])

    return render_template(
        "cart.html",
        products=products,
        total_price=total_price,
        total_products=total_products,
        out_of_stock_exist=out_of_stock_exist,
    )
