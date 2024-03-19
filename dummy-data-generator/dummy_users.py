from datetime import datetime

from werkzeug.security import generate_password_hash


def add_dummy_users(db, User):
    # dummy user 1
    user1 = User(
        type="customer",
        first_name="John",
        last_name="Doe",
        username="user1",
        email="john.doe@example.com",
        password=generate_password_hash("secret"),
        phone="1234567890",
        location="City, Country",
        gender="Male",
        date_of_birth=datetime(1990, 1, 1),
        weight=70.5,
        height=175.0,
        marital_status="Single",
        profile_image="customer.jpg",
    )
    db.session.add(user1)

    # dummy user 2
    user2 = User(
        type="admin",
        first_name="Jane",
        last_name="Smith",
        username="admin1",
        email="jane.smith@example.com",
        password=generate_password_hash("secret"),
        phone="9876543210",
        location="Another City, Country",
        gender="Female",
        date_of_birth=datetime(1985, 5, 10),
        weight=60.2,
        height=160.0,
        marital_status="Married",
        profile_image="admin.jpg",
    )
    # dummy user 3
    user3 = User(
        type="delivery_personel",
        first_name="David",
        last_name="Johnson",
        username="stuff1",
        email="david.johnson@example.com",
        password=generate_password_hash("secret"),
        phone="5555555555",
        location="City, Country",
        gender="Male",
        date_of_birth=datetime(1995, 3, 15),
        weight=80.0,
        height=185.0,
        marital_status="Single",
        profile_image="delivery_personel.jpg",
    )
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    # commit the changes to the database
    db.session.commit()
