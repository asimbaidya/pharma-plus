from flask import Blueprint, flash, redirect, render_template, url_for

from pharma_plus.models.user import User
from pharma_plus.utility.user_login_manager import customer_login_required
from pharma_plus.utility.user_session_manager import CurrentUser

notifications = Blueprint("notifications", __name__)
