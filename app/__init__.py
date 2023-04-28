# Python standard libraries
import os
import json
import datetime

# Third-party libraries
from flask import Flask, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import logger, auth


logger = logger.get(__name__)

#############
# Flask app #
#############

flask_app = Flask(__name__)
flask_app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


############
# Database #
############

db = SQLAlchemy()
flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shopper.db"
db.init_app(flask_app)

# Import models before creating database
from app.models import User

with flask_app.app_context():
    db.create_all()


###########
# Session #
###########

# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(flask_app)

# Flask-Login helper to load user
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

@flask_app.route("/")
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

@flask_app.route("/login")
def login():
    request_uri = auth.prepare_request_uri(request.base_url + "/callback")
    return redirect(request_uri)

@flask_app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    userinfo = auth.get_userinfo(code, request.url, request.base_url)
    # Make sure the email is verified
    if not userinfo or not userinfo.get("email_verified"):
        return "User email not available or not verified by Google.", 400
    # Parse user info
    user_id = userinfo.get("sub")
    user_name = userinfo.get("name")
    user_email = userinfo.get("email")
    user_picture = userinfo.get("picture")
    # Load or create user
    user = db.session.query(User).filter_by(id=user_id).first()
    current_time = datetime.datetime.now()
    if not user:
        user = User(id=user_id, name=user_name, email=user_email, picture=user_picture)
        user.created = current_time
        user.login_first = current_time
        db.session.add(user)
    user.login_latest = current_time
    db.session.commit()

    # Begin user session
    logger.info(f"Login {user}")
    login_user(user)

    # Redirect to homepage
    return redirect(url_for("index"))

@flask_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

