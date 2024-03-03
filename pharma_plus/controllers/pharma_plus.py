from flask import Blueprint, render_template

pharma_plus = Blueprint("pharma_plus", __name__)


@pharma_plus.route("/", methods=["GET"])
def home():
    # todo fetch all products
    return render_template("home.html")


@pharma_plus.route("/about", methods=["GET"])
def about():
    return render_template("about.html")
