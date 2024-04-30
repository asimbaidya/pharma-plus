from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from pharma_plus.models.user import User
from pharma_plus.utility.user_login_manager import customer_login_required
from pharma_plus.utility.user_session_manager import CurrentUser

customer = Blueprint("customer", __name__)


@customer.route("/profile/customer/<string:username>", methods=["GET", "POST"])
@customer_login_required
def profile(username):
    if username != CurrentUser.get_username():
        flash("Unauthorized access blocked", "error")
        return redirect(url_for("pharma_plus.home"))

    customer = User.query.filter_by(username=username).first()
    profile_image = url_for(
        "static", filename="media/customers/" + customer.profile_image
    )
    return render_template(
        "customer.html", profile_image=profile_image, customer=customer
    )
