# Python standard libraries
import os
import json
import logging
import sqlite3

# Third-party libraries
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

from app import auth

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

from app.user import User
from app.db import init_db_command
# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.picture
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'

@app.route("/login")
def login():
    request_uri = auth.prepare_request_uri(request.base_url + "/callback")
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    userinfo = auth.get_userinfo(code, request.url, request.base_url)
    print(userinfo)
    # Make sure the email is verified
    if not userinfo or not userinfo.get("email_verified"):
        return "User email not available or not verified by Google.", 400


    user_id = userinfo.get("sub")
    user_name = userinfo.get("name")
    user_email = userinfo.get("email")
    user_picture = userinfo.get("picture")
    user = User(user_id, user_name, user_email, user_picture)

    # Doesn't exist? Add it to the database.
    if not User.get(user_id):
        User.create(user_id, user_name, user_email, user_picture)

    # # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

