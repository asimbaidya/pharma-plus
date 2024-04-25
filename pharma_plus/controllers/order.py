from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from pharma_plus import db
from pharma_plus.models.product import Order, Payment
from pharma_plus.models.user import User
from pharma_plus.utility.user_login_manager import (
    admin_login_required,
    customer_login_required,
    delivery_personnel_login_required,
)
from pharma_plus.utility.user_session_manager import CurrentUser

orders = Blueprint("orders", __name__)


@orders.route("/order/active/<string:username>", methods=["GET", "POST"])
@customer_login_required
def active_orders(username):
    if username != CurrentUser.get_username():
        flash("Unauthorized access blocked", "error")
        return redirect(url_for("pharma_plus.home"))

    customer = User.query.filter_by(username=username).first()

    customer.profile_image = url_for(
        "static", filename="media/customers/" + customer.profile_image
    )

    orders = (
        Order.query.filter_by(customer_id=customer.id).filter_by(status="Pending").all()
    )

    for order in orders:
        delivery_personnel = User.query.filter_by(
            id=order.delivery_personnel_id
        ).first()

        order.delivery_personnel_name = (
            delivery_personnel.first_name + " " + delivery_personnel.last_name
        )
        order.delivery_personnel_image = url_for(
            "static",
            filename="media/delivery_personnels/" + delivery_personnel.profile_image,
        )

    return render_template("active_orders.html", customer=customer, orders=orders)


@orders.route("/order/history/<string:username>", methods=["GET"])
@customer_login_required
def order_history(username):
    if username != CurrentUser.get_username():
        flash("Unauthorized access blocked", "error")
        return redirect(url_for("pharma_plus.home"))

    customer = User.query.filter_by(username=username).first()

    customer.profile_image = url_for(
        "static", filename="media/customers/" + customer.profile_image
    )

    orders = (
        Order.query.filter_by(customer_id=customer.id)
        .filter_by(status="Completed")
        .all()
    )

    for order in orders:
        delivery_personnel = User.query.filter_by(
            id=order.delivery_personnel_id
        ).first()

        order.delivery_personnel_name = (
            delivery_personnel.first_name + " " + delivery_personnel.last_name
        )
        order.delivery_personnel_image = url_for(
            "static",
            filename="media/delivery_personnels/" + delivery_personnel.profile_image,
        )

    return render_template("orders_history.html", customer=customer, orders=orders)


@orders.route("/order/in-progress/<string:username>", methods=["GET", "POST"])
@delivery_personnel_login_required
def orders_in_progress(username):
    if username != CurrentUser.get_username():
        flash("Unauthorized access blocked", "error")
        return redirect(url_for("pharma_plus.home"))

    delivery_personnel = User.query.filter_by(username=username).first()

    orders = (
        Order.query.filter_by(delivery_personnel_id=delivery_personnel.id)
        .filter_by(status="Pending")
        .all()
    )

    for order in orders:
        customer = User.query.filter_by(id=order.delivery_personnel_id).first()

        order.delivery_personnel_name = customer.first_name + " " + customer.last_name
        order.delivery_personnel_image = url_for(
            "static",
            filename="media/delivery_personnels/" + delivery_personnel.profile_image,
        )

    return render_template(
        "orders-in-progress.html",
        orders=orders,
        delivery_personnel=delivery_personnel,
    )


@orders.route("/order/complete-delivery/<string:order_id>", methods=["POST"])
@delivery_personnel_login_required
def complete_delivery(order_id: str):

    order_id = int(order_id)
    order = Order.query.filter_by(id=order_id).first()
    verification_code = request.form["verification_code"]

    if verification_code == order.verification_code:
        order.status = "Completed"
        order.delivery_status = "Completed"
        order.complete_time_stamp = datetime.utcnow()
        db.session.commit()
        flash("Order completed successfully", "success")
    else:
        print(verification_code, order.verification_code)
        flash("Verification code is incorrect", "error")

    return redirect(
        url_for("orders.orders_in_progress", username=CurrentUser.get_username())
    )


@orders.route("/order/delivery_history/<string:username>", methods=["GET"])
@delivery_personnel_login_required
def delivery_history(username: str):
    if username != CurrentUser.get_username():
        flash("Unauthorized access blocked", "error")
        return redirect(url_for("pharma_plus.home"))

    delivery_personnel = User.query.filter_by(username=username).first()

    orders = (
        Order.query.filter_by(delivery_personnel_id=delivery_personnel.id)
        .filter_by(status="Completed")
        .all()
    )

    for order in orders:
        customer = User.query.filter_by(id=order.delivery_personnel_id).first()

        order.customer_name = customer.first_name + " " + customer.last_name
        order.customer_image = url_for(
            "static",
            filename="media/customers/" + customer.profile_image,
        )

    return render_template(
        "delivery_history.html", orders=orders, delivery_personnel=delivery_personnel
    )


@orders.route("/order/orders_report/", methods=["GET"])
@admin_login_required
def orders_report():

    orders = Order.query.order_by(Order.status).all()

    for order in orders:
        customer_id = order.customer_id
        delivery_personnel_id = order.delivery_personnel_id

        customer = User.query.filter_by(id=customer_id).first()
        delivery_personnel = User.query.filter_by(id=delivery_personnel_id).first()

        order.customer_name = customer.first_name + " " + customer.last_name
        order.customer_image = url_for(
            "static",
            filename="media/customers/" + customer.profile_image,
        )
        order.delivery_personnel_name = customer.first_name + " " + customer.last_name
        order.delivery_personnel_image = url_for(
            "static",
            filename="media/delivery_personnels/" + delivery_personnel.profile_image,
        )

    return render_template(
        "orders_report.html", orders=orders, delivery_personnel=delivery_personnel
    )
