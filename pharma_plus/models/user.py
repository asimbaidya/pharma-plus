from datetime import datetime

from flask import url_for
from werkzeug.security import check_password_hash

from pharma_plus import db
from pharma_plus.utility.user_cart_manager import Cart
from pharma_plus.utility.user_session_manager import CurrentUser


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # type (admin, customer, pharmacist)
    type = db.Column(db.String(20), nullable=False)

    # names data
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)

    # auth related data
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # contact data
    phone = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(255), nullable=True)

    # ddp - default display picture
    profile_image = db.Column(db.String(60), nullable=True, default="ddp.jpg")

    # preferences
    mail_notification = db.Column(db.Boolean, default=True)
    personalize_recom = db.Column(db.Boolean, default=True)
    subscription_offer = db.Column(db.Boolean, default=True)

    # health data
    gender = db.Column(db.String(10), nullable=True)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    marital_status = db.Column(db.String(20), nullable=True)

    # delivery_personnel specific data
    total_deliveries_in_progress = db.Column(db.Integer, nullable=True, default=0)

    @staticmethod
    def is_unique_email(new_email: str):
        return User.query.filter_by(email=new_email).first() is None

    @staticmethod
    def is_unique_username(new_username: str):
        return User.query.filter_by(username=new_username).first() is None

    @staticmethod
    def register(first_name, last_name, username, email, password, type="customer"):
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            type=type,
        )  # type: ignore
        db.session.add(user)
        db.session.commit()
        return True

    @staticmethod
    def verify_login(username, password, user_type):
        print(username)
        print(user_type)
        print(password)
        user: User = User.query.filter_by(username=username).first()
        print(user.type == user_type)
        print(user.type, user_type)
        if (
            user
            and check_password_hash(user.password, password)
            and user.type == user_type
        ):

            if user_type == "admin":
                profile_image = url_for(
                    "static", filename=f"media/admins/{user.profile_image}"
                )
            elif user_type == "customer":
                profile_image = url_for(
                    "static", filename=f"media/customers/{user.profile_image}"
                )
            else:
                profile_image = url_for(
                    "static", filename=f"media/delivery_personnels/{user.profile_image}"
                )
            CurrentUser.login(
                id=user.id,
                username=user.username,
                profile_image=profile_image,
                is_admin=user.type == "admin",
                is_customer=user.type == "customer",
                is_delivery_personnel=user.type == "delivery_personnel",
            )

            # if user is customer, iniiate a cart, so customer can add products
            if user.type == "customer":
                Cart.init_cart()

            return True
        return None


class RewardPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reward_points = db.Column(db.Integer, nullable=False)


subscription_product = db.Table(
    "subscription_product",
    db.Column("subscription_id", db.Integer, db.ForeignKey("subscription.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
)


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    count = db.Column(db.DateTime, nullable=False)
    total_course = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)

    #   now
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_order_date = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship(
        "Product", secondary=subscription_product, backref="subscribers"
    )
