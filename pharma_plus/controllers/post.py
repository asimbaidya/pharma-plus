from flask import Blueprint, flash, redirect, render_template, request, url_for

from pharma_plus import db
from pharma_plus.models.other import Post
from pharma_plus.models.user import User
from pharma_plus.utility.user_login_manager import customer_login_required
from pharma_plus.utility.user_session_manager import CurrentUser

posts = Blueprint("posts", __name__)


# create  post
@posts.route("/post/new", methods=["GET", "POST"])
@customer_login_required
def new_post():
    return render_template("create_post.html", title="New Post")


@posts.route("/post/create", methods=["POST"])
@customer_login_required
def create_post():
    post = request.form.get("post")
    customer = User.query.filter_by(username=CurrentUser.get_username()).first()

    new_post = Post(post=post, customer=customer.username)  # type: ignore
    db.session.add(new_post)
    db.session.commit()

    flash("Post created successfully", "success")
    return redirect(url_for("pharma_plus.home"))
