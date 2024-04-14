from dataclasses import dataclass

from flask import session


@dataclass
class CurrentUser:
    id: int
    username: str
    profile_image: str
    _is_authenticated: bool = False
    _is_customer: bool = False
    _is_admin: bool = False
    _is_delivery_personnel: bool = False

    @staticmethod
    def login(
        id,
        username,
        profile_image,
        is_admin=False,
        is_customer=False,
        is_delivery_personnel=False,
    ):
        session["current_user"] = CurrentUser(
            id,
            username,
            profile_image,
            _is_authenticated=True,
            _is_admin=is_admin,
            _is_customer=is_customer,
            _is_delivery_personnel=is_delivery_personnel,
        )
        return f"Logged in {username}"

    @staticmethod
    def is_authenticated():
        current_user = session.get("current_user")
        if current_user and current_user["_is_authenticated"]:
            return True
        else:
            return False

    @staticmethod
    def is_admin():
        current_user = session.get("current_user")
        if current_user and current_user["_is_admin"]:
            return True
        else:
            return False

    @staticmethod
    def is_customer():
        current_user = session.get("current_user")
        if current_user and current_user["_is_customer"]:
            return True
        else:
            return False

    @staticmethod
    def is_delivery_personnel():
        current_user = session.get("current_user")
        if current_user and current_user["_is_delivery_personnel"]:
            return True
        else:
            return False

    @staticmethod
    def get_username():
        current_user = session.get("current_user")
        if current_user and current_user["_is_authenticated"]:
            return current_user["username"]
        raise Exception("Can not get username, Not logged in")

    @staticmethod
    def get_id():
        current_user = session.get("current_user")
        if current_user and current_user["_is_authenticated"]:
            return current_user["id"]
        raise Exception("Can not get ID, Not logged in")

    @staticmethod
    def logout(username: str):
        print("logged out")
        session.clear()
        return f"Logged out {username}"

    @staticmethod
    def update_profile_image(profile_image: str):
        current_user = session.get("current_user")
        if current_user and current_user["_is_authenticated"]:
            current_user["profile_image"] = profile_image
            session["current_user"] = current_user
        raise Exception("Can not update profile image, Not logged in")

    @staticmethod
    def match_username(username: str):
        # considering this will be called with login required decorator, so current_user will be not None!
        current_user = session.get("current_user")
        return username == current_user["username"]
