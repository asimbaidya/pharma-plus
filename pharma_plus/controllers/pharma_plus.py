from flask import Blueprint, abort, render_template, url_for

from pharma_plus import db
from pharma_plus.models.other import Post
from pharma_plus.models.user import User
from pharma_plus.utility.user_session_manager import CurrentUser

pharma_plus = Blueprint("pharma_plus", __name__)


@pharma_plus.route("/", methods=["GET"])
def home():
    print(CurrentUser.is_delivery_personnel())
    print(CurrentUser._is_delivery_personnel)

    posts = db.session.query(Post).all()
    for post in posts:
        customer = User.query.filter_by(username=post.customer).first()
        if customer is None:
            abort(404)
        profile_image = url_for(
            "static", filename="media/customers/" + customer.profile_image
        )
        post.profile_image = profile_image  # type: ignore
    return render_template("home.html", title="Pharma Plus", posts=posts)


@pharma_plus.route("/about", methods=["GET"])
def about():
    return render_template("about.html")
