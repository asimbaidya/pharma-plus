from dataclasses import dataclass, field

from flask import abort, flash, redirect, session

from pharma_plus import db
from pharma_plus.models.product import Product


@dataclass
class Cart:
    total_product: int = 0
    total_price: int = 0
    added_product: list = field(default_factory=list)

    @staticmethod
    def init_cart():
        # this basically initilize a new cart into the users session, so new product can be added
        session["cart"] = Cart()

    @staticmethod
    def add_to_cart(product_id: int):
        product = db.session.query(Product).filter(Product.id == product_id).first()
        cart = session["cart"]

        if not cart:
            flash("Cart not found, Somethign went wrong in server")
            redirect("pharma_plus.home")

        if not product:
            flash("product not found, Somethign went wrong in server")
            redirect("pharma_plus.home")

        cart["added_product"].append(product_id)
        cart["total_product"] += 1
        cart["total_price"] += product.price

        session["cart"] = cart

    @staticmethod
    def remove_from_cart(product_id: int):
        # cart is not a pure dictionary only(not object)
        cart = session.get("cart")
        product = db.session.query(Product).filter(Product.id == product_id).first()

        if not cart:
            flash("Cart not found, Somethign went wrong in server")
            redirect("pharma_plus.home")

        if not product:
            flash("product not found, Somethign went wrong in server")
            redirect("pharma_plus.home")

        if product_id in cart["added_product"]:
            cart["added_product"].remove(product_id)
            cart["total_product"] -= 1
            cart["total_price"] -= product.price

            # now update the cart in session again
            session["cart"] = cart
            flash("product removed from cart")
        flash("product was not in the cart")

    @staticmethod
    def clear_cart():
        # cart is not a pure dictionary only(not object)
        cart = session.get("cart")

        if not cart:
            flash("Cart not found, Somethign went wrong in server")
            redirect("pharma_plus.home")

        # cleared(not deleted)
        cart["total_product"] = 0
        cart["total_price"] = 0
        cart["added_product"] = []

        # now update the cart in session again
        session["cart"] = cart

    @staticmethod
    def get_cart_items():
        cart = session.get("cart")

        if not cart:
            flash("Cart not found, Somethign went wrong in server")
            redirect("pharma_plus.home")

        total_price = 0
        for product_id in cart["added_product"]:
            product = db.session.query(Product).filter(Product.id == product_id).first()
            if not product:
                abort(404)
            total_price += product.price
        return cart["added_product"], total_price
