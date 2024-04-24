from flask import Blueprint, render_template, request, url_for

from pharma_plus.models.product import Product

search = Blueprint("search", __name__)


@search.route("/search", methods=["GET"])
def searches():
    return render_template("search.html")


@search.route("/search_results", methods=["GET"])
def search_results():
    search_query = request.args.get("search")
    sort = request.args.get("sort_order", "Ascending")

    if search_query.strip() == "":
        return render_template("search_results.html", products=[])

    products = Product.query.filter(Product.name.ilike(f"%{search_query}%")).all()

    # iterate over each product
    for product in products:
        # find the index of the search query in the product name
        index = product.name.lower().find(search_query.lower())

        # if search query is found in the product name
        if index != -1:
            # construct the modified product name with the matching part wrapped in a <span> tag
            # this is basically, highlighting the matching part of the product name
            # for readibility and user experience
            highlighted_name = (
                product.name[:index]
                + f"<span class='text-blue-500'>{product.name[index:index+len(search_query)]}</span>"
                + product.name[index + len(search_query) :]
            )

            # update the product with the highlighted name
            product.highlighted_name = highlighted_name

    if sort == "Descending":
        products = sorted(products, key=lambda x: x.name, reverse=True)

    for product in products:
        product.image_url = url_for(
            "static", filename=f"media/products/{product.image_url}"
        )
    return render_template("search_results.html", products=products)
