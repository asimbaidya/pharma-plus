from flask import Blueprint, redirect, render_template, session, url_for

users = Blueprint("users", __name__)


# Only customers will be able to register through this route
# admin, adn delivery personel will be added by the admin manually
# for extreme security measure :) & simplicity
@users.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


# however, all users will be able to login through this route
@users.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


# everyone will logout through this route
def logout():
    session.clear()
    return redirect(url_for("pharma_plus.home"))


@users.route("/user/<string:username>", methods=["GET"])
def user(username: str):
    return "<h1>Welcome to the admin profile</h1>"
