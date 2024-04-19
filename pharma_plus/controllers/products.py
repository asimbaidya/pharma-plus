from flask import Blueprint, flash, render_template, request

from pharma_plus.models.product import Product
from pharma_plus.utility.file_path_manager import save_image_to_static_folder
from pharma_plus.utility.user_login_manager import admin_login_required

products = Blueprint("products", __name__)


@products.route("/product/add", methods=["GET", "POST"])
@admin_login_required
def add_new():
    if request.method == "POST":
        name = request.form.get("name")
        brand_name = request.form.get("brand_name")
        description = request.form.get("description")
        image = request.files["image"]
        price = float(request.form.get("price"))
        stock = int(request.form.get("stock"))
        category = request.form.get("category")
        generic_name = request.form.get("generic_name")
        dosage = request.form.get("dosage")
        side_effects = request.form.get("side_effects")
        is_medicine = bool(request.form.get("is_medicine"))
        is_prescription_required = bool(request.form.get("is_prescription_required"))
        is_supplement = bool(request.form.get("is_supplement"))

        img_file_name = save_image_to_static_folder(
            img_file=image, folder_name="products"
        )

        Product.add_to_inventory(
            name=name,
            brand_name=brand_name,
            description=description,
            image_url=img_file_name,
            price=price,
            stock=stock,
            category=category,
            generic_name=generic_name,
            dosage=dosage,
            side_effects=side_effects,
            is_medicine=is_medicine,
            is_prescription_required=is_prescription_required,
            is_supplement=is_supplement,
        )
        flash("Product added successfully", "success")

    return render_template("product-add.html")


@products.route("/product/update/<int:product_id>", methods=["GET"])
@admin_login_required
def inventory_update(product_id: int):
    # verify if the product exists
    return f"<h1>ID {product_id}</h1>"


@products.route("/product/<int:product_id>", methods=["GET"])
def product(product_id: int):
    # verify if the product exists
    return f"<h1>ID {product_id}</h1>"


@products.route("/products/", methods=["GET"])
def product_browser():
    products = Product.query.all()
    print(products)
    return render_template("product-browser.html", products=products)
