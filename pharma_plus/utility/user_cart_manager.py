from dataclasses import dataclass, field

from flask import abort, flash, redirect, session

from pharma_plus import db
from pharma_plus.models.product import Product


@dataclass
class Cart:

    @staticmethod
    def init_cart():
        # this basically initilize a new cart(aka dict) into the users session, so new product can be added
        session["cart"] = {}

    @staticmethod
    def add_to_cart(product_id: str):
        cart = session["cart"]

        # values,key are str because session serialize those into s tr
        cart[product_id] = "1"
        session["cart"] = cart
        return True

    @staticmethod
    def increase(product_id: str):
        cart = session["cart"]

        # values,key are str because session serialize those into s tr
        current_value = int(cart[product_id])
        cart[product_id] = str(current_value + 1)
        session["cart"] = cart
        return True

    @staticmethod
    def decrease(product_id: str):
        cart = session["cart"]

        # values,key are str because session serialize those into s tr
        current_value = int(cart[product_id])

        if current_value == 1:
            del cart[product_id]
        else:
            cart[product_id] = str(current_value - 1)
        session["cart"] = cart
        return True

    @staticmethod
    def is_product_in_cart(product_id: int):
        product_id = str(product_id)
        cart = session["cart"]
        print("Here??")
        print(product_id in cart)
        print(cart)
        print(product_id)
        return product_id in cart

    def get_product_quantity(product_id: int):
        product_id = str(product_id)
        cart = session["cart"]
        return cart[product_id]

    @staticmethod
    def clear_cart():
        session["cart"] = {}
