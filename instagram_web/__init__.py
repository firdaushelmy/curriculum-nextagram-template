from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_login import LoginManager
from models.user import User
from flask_wtf.csrf import CSRFProtect
import config
import os
from instagram_web.util.googleauth import oauth


assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(images_blueprint, url_prefix="/images")

csrf = CSRFProtect()
csrf.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

oauth.init_app(app)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')


@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)
