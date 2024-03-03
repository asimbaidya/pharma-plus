import os
import sys

# this 3 line, make it possible to import db,app and other stuff without extra hassle
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from dummy_products import add_dummy_products
from dummy_users import add_dummy_users

if __name__ == "__main__":
    from pharma_plus import db
    from pharma_plus.models.other import (
        Analytics,
        Delivery,
        Feedback,
        Notification,
        ProductSuggestion,
    )
    from pharma_plus.models.product import Order, Payment, Prescription, Product
    from pharma_plus.models.user import RewardPoints, Subscription, User
    from run import app

    app.app_context().push()
    db.create_all()

    print(f"{Analytics.__name__} table was created successfully!")
    print(f"{Delivery.__name__} table was created successfully!")
    print(f"{Feedback.__name__} table was created successfully!")
    print(f"{Notification.__name__} table was created successfully!")
    print(f"{ProductSuggestion.__name__} table was created successfully!")
    print(f"{Order.__name__} table was created successfully!")
    print(f"{Payment.__name__} table was created successfully!")
    print(f"{Prescription.__name__} table was created successfully!")
    print(f"{Product.__name__} table was created successfully!")
    print(f"{RewardPoints.__name__} table was created successfully!")
    print(f"{Subscription.__name__} table was created successfully!")
    print(f"{User.__name__} table was created successfully!")

    print("Creating dummy data...")

    add_dummy_users(db=db, User=User)
    add_dummy_products(db=db, Product=Product)

    # Commit the changes to the database
    db.session.commit()
