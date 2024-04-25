from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from pharma_plus.models.user import User
from pharma_plus.utility.user_session_manager import CurrentUser

users = Blueprint("users", __name__)


# Only customers will be able to register through this route
# admin, adn delivery personel will be added by the admin manually
# for extreme security measure :) & simplicity


@users.route("/register", methods=["GET", "POST"])
def register():
    if CurrentUser.is_authenticated():
        flash("You are alread logged in!", "info")
        return redirect(url_for("pharma_plus.home"))

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        if not User.is_unique_username(username):
            flash("A User with same username already exists", "info")
            return redirect(url_for("users.register"))
        if not User.is_unique_email(email):
            flash("Email already exists", "info")
            return redirect(url_for("users.register"))

        # all good
        if User.register(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_password,
        ):
            flash("Account created successfully", "info")
            return redirect(url_for("users.login"))
        else:
            flash("Server error! Please  try again :(", "info")

    return render_template("register.html")


# however, all users will be able to login through this route
@users.route("/login", methods=["GET", "POST"])
def login():
    if CurrentUser.is_authenticated():
        flash("You are alread logged in!", "info")
        return redirect(url_for("pharma_plus.home"))

    if request.method == "POST":
        username = request.form["username"]
        passsword = request.form["password"]
        user_type = request.form["user_type"]

        print(user_type)

        login_success: bool = User.verify_login(
            username=username, password=passsword, user_type=user_type
        )

        if login_success:
            flash("Your are Logged in Successfully!", "success")
            return redirect(url_for("pharma_plus.home"))
        else:
            flash("Invalid Credential", "error")
    return render_template("login.html")


# everyone will logout through this route
@users.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("logged Out Succesfully!", "info")
    return redirect(url_for("pharma_plus.home"))


@users.route("/user/<string:username>", methods=["GET"])
def user(username: str):
    return "<h1>Welcome to the admin profile</h1>"
