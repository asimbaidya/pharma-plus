from distutils.command import register

from pharma_plus import db


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

    @staticmethod
    def is_unique_email(new_email: str):
        return User.query.filter_by(email=new_email).first() is None

    @staticmethod
    def is_unique_username(new_username: str):
        return User.query.filter_by(username=new_username).first() is None

    @staticmethod
    def register(type, first_name, last_name, username, email, password):
        user = User(
            type=type,
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )  # type: ignore
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def verify_login(ype, username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.password == password and user.type == type:
            return user
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

    start_date = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True)

    products = db.relationship(
        "Product", secondary=subscription_product, backref="subscribers"
    )
