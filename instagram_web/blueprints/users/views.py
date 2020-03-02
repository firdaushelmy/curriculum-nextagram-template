import re
from flask import Blueprint, render_template, request, flash, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from flask_login import login_required, current_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')
    pass


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/<id>/edit', methods=["GET"])
@login_required
def index():
    users = User.select()
    return render_template('users/index.html', users=users)


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    if not str(current_user.id) == id:  # this is the current user
        flash('you are not authorised to view this page fool', 'danger')
        # return redirect(url_for('users.index'))
    user = User.get_or_none(User.id == id)
    if not user:
        flash('No user found with with the provided ID', 'warning')
        return redirect(url_for('users.index'))

    return render_template('users/editprofile.html', user=user)


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_or_none(User.id == id)

    if not user:
        flash('no user found with id provided', 'warning')
        return redirect(url_for('users.index'))

    email = request.form.get('email')
    username = request.form.get('username')

    user.email = email
    user.username = username

    if not user.save():
        for error in user.errors:
            flash(error, 'warning')
        return redirect(url_for('users.edit', id=user.id))

    flash('Successfully updated your details', 'success')
    return redirect(url_for('users.templates.users.editprofile', id=user.id))
