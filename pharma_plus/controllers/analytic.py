from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, url_for
from sqlalchemy import asc, func

from pharma_plus import db
from pharma_plus.models.product import Inventory, Order, Product
from pharma_plus.models.user import User
from pharma_plus.utility.user_login_manager import (
    admin_login_required,
    customer_login_required,
)
from pharma_plus.utility.user_session_manager import CurrentUser

analytics = Blueprint("analytics", __name__)


@analytics.route("/sells_analytics", methods=["GET"])
@admin_login_required
def sells_analytics():
    # Query the database for sales data

    return render_template(
        "sells_analytics.html",
    )


@analytics.route("/all_inventories", methods=["GET"])
@admin_login_required
def all_inventories():
    now = datetime.now()
    inventory_by_expire_date = (
        Inventory.query.order_by(asc(Inventory.expire_date))
        .filter(Inventory.expire_date > now)
        .all()
    )

    for inventory in inventory_by_expire_date:
        product = Product.query.filter_by(id=inventory.product_id).first()
        inventory.product = product

    print(">>>")
    print(inventory_by_expire_date)

    return render_template("all_inventory.html", inventories=inventory_by_expire_date)


@analytics.route("/expired_inventory", methods=["GET"])
@admin_login_required
def expired_inventory():

    now = datetime.now()
    # Query the database for expired medicines
    expired_inventories = Inventory.query.filter(Inventory.expire_date < now).all()

    for inventory in expired_inventories:
        product = Product.query.filter_by(id=inventory.product_id).first()
        inventory.product = product

    print(">>>")
    print(expired_inventories)

    return render_template(
        "expired_inventory.html", expired_inventories=expired_inventories
    )


@analytics.route("/users")
@admin_login_required
def all_users():
    users = User.query.order_by(asc(User.type)).all()

    for user in users:
        if user.type == "admin":
            user.profile_image = url_for(
                "static", filename=f"media/admins/{user.profile_image}"
            )
            user.total_order = "N/A"
        elif user.type == "customer":
            user.profile_image = url_for(
                "static", filename=f"media/customers/{user.profile_image}"
            )
            user.total_order = len(Order.query.filter_by(customer_id=user.id).all())
        else:
            user.total_order = len(
                Order.query.filter_by(delivery_personnel_id=user.id).all()
            )
    return render_template("all_users.html", users=users)
