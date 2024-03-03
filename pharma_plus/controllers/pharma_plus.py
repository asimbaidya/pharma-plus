from flask import Blueprint, render_template

pharma_plus = Blueprint("pharma_plus", __name__)


@pharma_plus.route("/", methods=["GET"])
def home():
    return render_template("default-home.html")
