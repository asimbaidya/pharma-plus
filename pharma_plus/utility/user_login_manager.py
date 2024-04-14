from functools import wraps

from flask import flash, redirect

from pharma_plus.utility.user_session_manager import CurrentUser


def admin_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if CurrentUser.is_admin():
            return func(*args, **kwargs)
        else:
            flash("Access denied. Admin login required, Visit Home instead", "warning")
            return redirect("/")

    return wrapper


def customer_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if CurrentUser.is_customer():
            return func(*args, **kwargs)
        else:
            flash("Access denied. Admin login required, Visit Home instead", "warning")
            return redirect("/")

    return wrapper


def delivery_personnel_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if CurrentUser.is_delivery_personnel():
            return func(*args, **kwargs)
        else:
            flash(
                "Access denied. delivery_personnel login required, Visit Home instead",
                "warning",
            )
            return redirect("/")

    return wrapper


# # alternative with one decorator(nested)
# # but can not customize flash message
# def login_required(user_type):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             if user_type == "admin" and CurrentUser.is_admin():
#                 return func(*args, **kwargs)
#             elif user_type == "customer" and CurrentUser.is_customer():
#                 return func(*args, **kwargs)
#             elif (
#                 user_type == "delivery_personnel"
#                 and CurrentUser.is_delivery_personnel()
#             ):
#                 return func(*args, **kwargs)
#             else:
#                 flash(
#                     f"Access denied. {user_type} login required, Visit Home instead",
#                     "warning",
#                 )
#                 return redirect("/")
#         return wrapper
#     return decorator
