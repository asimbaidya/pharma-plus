from datetime import datetime

from pharma_plus import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # basic product information
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)

    # related to sells
    stock = db.Column(db.Integer, nullable=True)

    # brand info
    brand_name = db.Column(db.String(120), nullable=True)

    # medicine specific attributes (optional)
    category = db.Column(db.String(120), nullable=True)
    generic_name = db.Column(db.String(120), nullable=True)
    is_medicine = db.Column(db.Boolean, default=False)
    strength = db.Column(db.String(120), nullable=True)

    # additional fields (optional)
    dosage = db.Column(db.String(120), nullable=True)
    side_effects = db.Column(db.Text, nullable=True)
    uses = db.Column(db.Text, nullable=True)

    # Supplement specific attributes (optional)
    is_supplement = db.Column(db.Boolean, default=False)
    supplement_type = db.Column(db.String(120), nullable=True)
    inventory = db.relationship("Inventory", backref="product", lazy=True)

    @staticmethod
    def save_product_image(image):
        image.save("static/media/products/" + image.filename)
        return "/static/images/" + image.filename

    @staticmethod
    def add_to_inventory(
        stock,
        name,
        brand_name,
        description,
        image_url,
        price,
        category,
        generic_name,
        dosage,
        side_effects,
        is_medicine,
        is_supplement,
    ):
        for _ in range(stock):
            new_product = Product(
                name=name,
                brand_name=brand_name,
                description=description,
                image_url=image_url,
                price=price,
                category=category,
                generic_name=generic_name,
                dosage=dosage,
                side_effects=side_effects,
                is_medicine=is_medicine,
                is_supplement=is_supplement,
            )
            db.session.add(new_product)
            db.session.commit()

    @staticmethod
    def update_inventory(product_id, new_stock):
        product = Product.query.get(product_id)
        if product:
            product.stock += new_stock
            db.session.commit()
        raise Exception("Product not found")


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    expire_date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    # basic info
    id = db.Column(db.Integer, primary_key=True)

    # delivery
    order_delivery_date = db.Column(db.DateTime, nullable=False)
    order_received_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    order_complated_timestamp = db.Column(db.DateTime, nullable=True)
    delivery_address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    delivery_personel_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=True
    )

    # payment
    status = db.Column(db.String(20), nullable=False)
    total_items = db.Column(db.Integer, nullable=False)
    total_bill = db.Column(db.Integer, nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"))
    verification_code = db.Column(db.String(10), nullable=False)

    # new method
    products = db.relationship("OrderProduct", backref="order", lazy=True)


class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False, default="cash")
    payment_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
