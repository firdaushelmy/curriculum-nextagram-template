import re
import os
import config
from flask import Flask, request, render_template, flash, redirect, url_for
from models.base_model import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc


@app.route("/SignIn/")
def sign_in():
    return render_template('user_signin.html')


@app.route("/SignIn", methods=["POST"])
def create_user():
    password = request.form['password_form']
    if len(password) > 6 and re.search(r"[a-zA-Z]", password) and re.search(r"[\W]", password):
        hashed_password = generate_password_hash(password)
        u = User(
            username=request.form['username_form'],
            email=request.form['email_form'],
            password=hashed_password)
        try:
            u.save()
            flash('Successfully created account! NOICE!')
            return redirect(url_for('sign_in'))
        except:
            return render_template('user_signin.html', name=request.form['username_form'])
    else:
        flash("EH CBAI DO PROPERLY CAN OR NOT?")
        return redirect(url_for('sign_in'))
