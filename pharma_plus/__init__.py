from flask import Flask

from pharma_plus.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(Config)

    # impurts all blueprint(rouutes)
    from pharma_plus.controllers.pharma_plus import pharma_plus

    # register blueprint
    app.register_blueprint(pharma_plus)

    return app
    return app
