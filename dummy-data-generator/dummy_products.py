from datetime import datetime


def add_dummy_products(db, Product, Inventory):
    # dummy product 1
    product1 = Product(
        name="Pain Relief Tablets",
        description="Effective pain relief for various conditions.",
        image_url="pain_relief.jpeg",
        price=15.99,
        brand_name="HealthCare",
        category="Pain Relief",
        generic_name="Ibuprofen",
        is_medicine=True,
        strength="500mg",
        dosage="Take one tablet every 4-6 hours",
        side_effects="May cause drowsiness",
        uses="Relief from mild to moderate pain",
    )

    # dummy product 2
    product2 = Product(
        name="Vitamin C Supplement",
        description="Boosts immunity and promotes overall health.",
        image_url="vitamin_c_supplement.jpg",
        price=9.99,
        brand_name="NutriLife",
        category="Vitamins",
        is_supplement=True,
        supplement_type="Vitamin C",
    )

    # dummy product 3
    product3 = Product(
        name="Allergy Relief Syrup",
        description="Relieves symptoms of seasonal allergies.",
        image_url="allergy_relief_syrup.jpg",
        price=12.99,
        brand_name="WellnessCare",
        category="Allergy Relief",
        generic_name="Cetirizine",
        is_medicine=True,
        strength="5mg",
        dosage="Take 10ml once daily",
        side_effects="May cause drowsiness",
        uses="Relief from allergy symptoms",
    )

    # dummy product 4
    product4 = Product(
        name="Digestive Enzyme Tablets",
        description="Aids in digestion and promotes gut health.",
        image_url="digestive_enzyme_tablets.jpeg",
        price=8.49,
        brand_name="GutWell",
        category="Digestive Health",
        is_supplement=True,
        supplement_type="Digestive Enzymes",
    )

    # dummy product 5
    product5 = Product(
        name="Antibacterial Hand Sanitizer",
        description="Kills germs and bacteria on hands.",
        image_url="hand_sanitizer.jpg",
        price=5.99,
        brand_name="CleanHands",
        is_medicine=False,
    )

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(product4)
    db.session.add(product5)
    # commit the changes to the database
    db.session.commit()

    inventory1 = Inventory(
        product_id=product1.id, quantity=15, expire_date=datetime(2024, 5, 25)
    )
    inventory2 = Inventory(
        product_id=product2.id, quantity=15, expire_date=datetime(2024, 5, 25)
    )

    inventory3 = Inventory(
        product_id=product3.id, quantity=15, expire_date=datetime(2024, 5, 25)
    )

    inventory4 = Inventory(
        product_id=product4.id, quantity=15, expire_date=datetime(2024, 5, 25)
    )

    inventory5 = Inventory(
        product_id=product5.id, quantity=15, expire_date=datetime(2024, 5, 25)
    )

    db.session.add(inventory1)
    db.session.add(inventory2)
    db.session.add(inventory3)
    db.session.add(inventory4)
    db.session.add(inventory5)

    # commit the changes to the database
    db.session.commit()
