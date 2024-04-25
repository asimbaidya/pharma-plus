from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from pharma_plus.models.user import User
from pharma_plus.utility.user_login_manager import admin_login_required
from pharma_plus.utility.user_session_manager import CurrentUser

admin = Blueprint("admin", __name__)


@admin.route("/profile/admin/<string:username>", methods=["GET", "POST"])
@admin_login_required
def profile(username):
    if username != CurrentUser.get_username():
        flash("Unauthorized access blocked", "error")
        return redirect(url_for("pharma_plus.home"))

    admin = User.query.filter_by(username=username).first()
    profile_image = url_for(
        "static",
        filename="media/delivery_personnels/" + admin.profile_image,
    )
    return render_template("admin.html", profile_image=profile_image, admin=admin)
