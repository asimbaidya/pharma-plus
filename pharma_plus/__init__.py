from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from pharma_plus.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # impurts all blueprint(rouutes)
    from pharma_plus.controllers.pharma_plus import pharma_plus

    # register blueprint
    app.register_blueprint(pharma_plus)

    from pharma_plus.models.other import (
        Analytics,
        Delivery,
        Feedback,
        Notification,
        ProductSuggestion,
    )
    from pharma_plus.models.product import (
        Order,
        Payment,
        PrescribedOrder,
        Prescription,
        Product,
    )
    from pharma_plus.models.user import (
        RewardPoints,
        Subscription,
        SubscriptionProduct,
        User,
    )

    print("These Flowing are the models of This Application")
    # Print table names for models in other
    for model in [Analytics, Delivery, Feedback, Notification, ProductSuggestion]:
        print(f"Table Name: {model.__name__}")

    # Print table names for models in product
    for model in [Order, Payment, PrescribedOrder, Prescription, Product]:
        print(f"Table Name: {model.__name__}")

    # Print table names for models in user
    for model in [RewardPoints, Subscription, SubscriptionProduct, User]:
        print(f"Table Name: {model.__name__}")

    return app
