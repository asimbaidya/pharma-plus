from ast import Try
from datetime import datetime

from pharma_plus import db

order_product = db.Table(
    "order_product",
    db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # basic product information
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)

    # related to sells
    stock = db.Column(db.Integer, nullable=False)
    monthly_sell_frequency = db.Column(db.Integer, nullable=True)
    stock_alert = db.Column(db.Integer, nullable=True)

    # brand info
    brand_name = db.Column(db.String(120), nullable=True)

    # medicine specific attributes (optional)
    category = db.Column(db.String(120), nullable=True)
    generic_name = db.Column(db.String(120), nullable=True)
    is_medicine = db.Column(db.Boolean, default=False)
    is_prescription_required = db.Column(db.Boolean, default=False)
    strength = db.Column(db.String(120), nullable=True)

    # additional fields (optional)
    dosage = db.Column(db.String(120), nullable=True)
    side_effects = db.Column(db.Text, nullable=True)
    uses = db.Column(db.Text, nullable=True)

    # Supplement specific attributes (optional)
    is_supplement = db.Column(db.Boolean, default=False)
    supplement_type = db.Column(db.String(120), nullable=True)

    @staticmethod
    def add_to_inventory(
        name, price, category, uses, is_supplement, supplement_type=None, image_url=None
    ):
        new_product = Product(
            name=name,
            price=price,
            category=category,
            uses=uses,
            is_supplement=is_supplement,
            supplement_type=supplement_type,
            image_url=image_url,
        )  # type: ignore
        db.session.add(new_product)
        db.session.commit()

    @staticmethod
    def add_stock(product_id, new_stock):
        product = Product.query.get(product_id)
        if product:
            product.stock += new_stock
            db.session.commit()
        raise Exception("Product not found")


class Order(db.Model):
    # basic info
    id = db.Column(db.Integer, primary_key=True)

    # delivery
    order_delivery_date = db.Column(db.DateTime, nullable=False)
    order_received_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    order_complated_timestamp = db.Column(db.DateTime, nullable=True)
    delivery_address = db.Column(db.String(255), nullable=False)

    # payment
    status = db.Column(db.String(20), nullable=False)
    total_bil = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)

    # product
    products = db.relationship("Product", secondary="order_product")


class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
