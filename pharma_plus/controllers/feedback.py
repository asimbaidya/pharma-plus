from flask import Blueprint, flash, redirect, render_template, url_for

from pharma_plus.models.user import User
from pharma_plus.utility.user_login_manager import customer_login_required
from pharma_plus.utility.user_session_manager import CurrentUser

feedbacks = Blueprint("feedbacks", __name__)
