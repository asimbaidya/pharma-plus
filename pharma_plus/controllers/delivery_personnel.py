from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from pharma_plus.models.user import User
from pharma_plus.utility.user_login_manager import delivery_personnel_login_required
from pharma_plus.utility.user_session_manager import CurrentUser

delivery_personnel = Blueprint("delivery_personnel", __name__)


@delivery_personnel.route("/profile/dp/<string:username>", methods=["GET", "POST"])
@delivery_personnel_login_required
def profile(username):
    if username != CurrentUser.get_username():
        flash("Unauthorized access blocked", "error")
        return redirect(url_for("pharma_plus.home"))

    delivery_personnel = User.query.filter_by(username=username).first()
    profile_image = url_for(
        "static",
        filename="media/delivery_personnels/" + delivery_personnel.profile_image,
    )

    return render_template(
        "delivery_personnel.html",
        profile_image=profile_image,
        delivery_personnel=delivery_personnel,
    )
