from flask import Blueprint

pharma_plus = Blueprint("pharma_plus", __name__)


@pharma_plus.route("/", methods=["GET"])
def home():
    return "<h1>Welcome To Pharmas Plus!</h1>"
