import random
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import asc

from pharma_plus import db
from pharma_plus.models.product import Inventory, Order, OrderProduct, Product
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
        inventories = Inventory.query.filter_by(product_id=product.id).all()
        product.stock = sum([inventory.quantity for inventory in inventories])

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


@cart.route("/place_order", methods=["GET", "POST"])
@customer_login_required
def place_order():

    delivery_address = request.form["delivery_address"]
    phone_number = request.form["phone_number"]

    # as all payment method are cash on delivery, this is not requried at the moment
    __payment_method = request.form["payment_method"]

    # getting the username from CurrnetUser and then fetching the customer object
    username = CurrentUser.get_username()
    customer = db.session.query(User).filter_by(username=username).first()

    cart = session["cart"]
    # Fetch products from database based on provided product ids
    products = (
        db.session.query(Product)
        .filter(Product.id.in_([int(k) for k in cart.keys()]))
        .all()
    )

    # Calculate total items and total bill
    total_items = len(products)
    total_bill = sum(product.price for product in products)

    for product in products:
        total_quantity_required = int(cart[str(product.id)])

        # Fetch all inventories that have quantity more than 0 and sort them based on expire_date
        inventories = (
            Inventory.query.filter_by(product_id=product.id)
            .filter(Inventory.quantity > 0)
            .order_by(asc(Inventory.expire_date))
            .all()
        )

        for inventory in inventories:
            if total_quantity_required > 0:
                # Decrease total_quantity_required from inventory
                decrease_quantity = min(total_quantity_required, inventory.quantity)
                inventory.quantity -= decrease_quantity
                total_quantity_required -= decrease_quantity

    # Create a new order object
    order = Order(
        order_delivery_date=datetime.utcnow(),
        delivery_address=delivery_address,
        phone_number=phone_number,
        customer_id=customer.id,
        total_items=total_items,
        status="Pending",
        total_bill=total_bill,
        verification_code=random.randint(1000000000, 9999999999),
        # products=products,
    )

    # now find delivery personnels who are not busy and then assign
    delivery_personnels = (
        User.query.filter_by(type="delivery_personnel")
        .order_by(asc(User.total_deliveries_in_progress))
        .first()
    )

    order.delivery_personnel_id = delivery_personnels.id

    # add the order to the database session
    db.session.add(order)
    db.session.commit()

    # now add quantity information to database
    for product in products:
        order_product = OrderProduct(
            order_id=order.id,
            product_id=product.id,
            quantity=cart[str(product.id)],
        )
        db.session.add(order_product)
        db.session.commit()

    session["cart"] = {}

    flash("Order Placed", "success")
    return redirect(url_for("pharma_plus.home"))
