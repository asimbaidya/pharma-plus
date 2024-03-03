from pharma_plus import db


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    delivery_person_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    tracking_info = db.Column(db.String(255), nullable=True)
    send_every_update_notification = db.Column(db.Boolean, default=True)


# notification are generated by system
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    read = db.Column(db.Boolean, default=False)


class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    total_sales = db.Column(db.Float, nullable=False)
    total_orders = db.Column(db.Integer, nullable=False)
    most_sold_product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=True
    )
    least_sold_product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=True
    )


class ProductSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    suggested_product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False
    )
    suggested_at = db.Column(db.DateTime, nullable=False)
