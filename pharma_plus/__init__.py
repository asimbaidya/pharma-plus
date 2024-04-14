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
    from pharma_plus.controllers.admin import admin
    from pharma_plus.controllers.customer import customer
    from pharma_plus.controllers.delivery_personnel import delivery_personnel
    from pharma_plus.controllers.pharma_plus import pharma_plus
    from pharma_plus.controllers.products import products
    from pharma_plus.controllers.search import search
    from pharma_plus.controllers.users import users

    # register blueprint
    app.register_blueprint(admin)
    app.register_blueprint(customer)
    app.register_blueprint(delivery_personnel)
    app.register_blueprint(pharma_plus)
    app.register_blueprint(products)
    app.register_blueprint(search)
    app.register_blueprint(users)

    from pharma_plus.models.other import (
        Analytics,
        Delivery,
        Feedback,
        Notification,
        ProductSuggestion,
    )
    from pharma_plus.models.product import Order, Payment, Prescription, Product
    from pharma_plus.models.user import RewardPoints, Subscription, User

    print("These Flowing are the models of This Application")
    # Print table names for models in other
    for model in [Analytics, Delivery, Feedback, Notification, ProductSuggestion]:
        print(f"Table Name: {model.__name__}")

    # Print table names for models in product
    for model in [Order, Payment, Prescription, Product]:
        print(f"Table Name: {model.__name__}")

    # Print table names for models in user
    for model in [RewardPoints, Subscription, User]:
        print(f"Table Name: {model.__name__}")

    return app
