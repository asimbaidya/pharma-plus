from flask import Blueprint, flash, redirect, render_template, request, url_for

from pharma_plus.models.product import Inventory, Product
from pharma_plus.utility.file_path_manager import save_image_to_static_folder
from pharma_plus.utility.user_cart_manager import Cart
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
        expire_date = request.form.get("expire_date")
        category = request.form.get("category")
        generic_name = request.form.get("generic_name")
        dosage = request.form.get("dosage")
        side_effects = request.form.get("side_effects")
        is_medicine = bool(request.form.get("is_medicine"))
        is_supplement = bool(request.form.get("is_supplement"))

        img_file_name = save_image_to_static_folder(
            img_file=image, folder_name="products"
        )

        Product.add_to_inventory(
            brand_name=brand_name,
            category=category,
            description=description,
            dosage=dosage,
            expire_date=expire_date,
            generic_name=generic_name,
            image_url=img_file_name,
            is_medicine=is_medicine,
            is_supplement=is_supplement,
            name=name,
            price=price,
            side_effects=side_effects,
            stock=stock,
        )
        flash("Product added successfully", "success")

    return render_template("product-add.html")


@products.route("/product/update/<int:product_id>", methods=["POST"])
@admin_login_required
def add_inventory(product_id: int):
    expire_date = request.form.get("expire_date")
    new_stock = request.form.get("new_stock")

    Product.add_inventory(
        product_id=product_id, expire_date=expire_date, new_stock=new_stock
    )
    return redirect(url_for("products.product", product_id=product_id))


@products.route("/product/<int:product_id>", methods=["GET"])
def product(product_id: int):
    # verify if the product exists
    product = Product.query.filter_by(id=product_id).first()
    product.image_url = url_for(
        "static", filename=f"media/products/{product.image_url}"
    )
    inventories = Inventory.query.filter_by(product_id=product.id).all()
    product.stock = sum([inventory.quantity for inventory in inventories])

    return render_template("product.html", product=product, Cart=Cart)


@products.route("/products/", methods=["GET"])
def product_browser():
    products = Product.query.all()
    for product in products:
        product.image_url = url_for(
            "static", filename=f"media/products/{product.image_url}"
        )

    return render_template("product-browser.html", products=products, Cart=Cart)
