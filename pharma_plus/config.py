class Config:
    SECRET_KEY = "DzlodszsZGo5+XitnLqRy8+gBh0nmdLp55c0nvZzmD9WiYcC79gJ"
    SQLALCHEMY_DATABASE_URI = "sqlite:///pharma_plus.db"
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # todo(use environmental vars)
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
