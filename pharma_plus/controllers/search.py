from flask import Blueprint, render_template, request

search = Blueprint("search", __name__)


@search.route("/search", methods=["GET"])
def searches():
    query = request.args.get("query")
    return render_template("search.html")
