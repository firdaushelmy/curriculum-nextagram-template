from config import S3_LINK
from playhouse.hybrid import hybrid_property
from flask import url_for
from flask_login import UserMixin
import re
import peewee as pw
from models.base_model import BaseModel
from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_login import LoginManager
from models.user import User


assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


------------


class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)
    profile_image = pw.CharField(null=True, default=None)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        if duplicate_username and not duplicate_username.id == self.id:
            self.errors.append('Username not unique boo')
        duplicate_email = User.get_or_none(User.email == self.email)
        if duplicate_email and not duplicate_email.id == self.id:
            self.errors.append('Email not unique boo')

    @hybrid_property
    def profile_image_url(self):
        if self.profile_image:
            return f"{S3_LINK}/{self.profile_image}"
        else:
            return url_for("static", filename="pichas/default.jpg")
