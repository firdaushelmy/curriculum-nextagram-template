import re
from flask import Blueprint, render_template, request, flash, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from flask_login import login_user, login_required, logout_user, current_user
from helper import upload_file_to_s3
from config import S3_BUCKET, S3_LOCATION

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/<id>/edit', methods=["GET"])
@login_required
def index(id):
    users = User.select()
    return render_template('users/editprofile.html', users=users)


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    if not str(current_user.id) == id:  # this is the current user
        flash('you are not authorised to view this page fool', 'danger')
        # return redirect(url_for('users.index'))
    else:
        user = User.get_or_none(User.id == id)
        if not user:
            flash('No user found with with the provided ID', 'warning')
        else:
            return render_template('users/editprofile.html', user=user)


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    if not str(current_user.id) == id:
            # need to validate the signed in id
        flash("errr dont think you are authorised to access this")
        return redirect(url_for('users.edit', id=id))
    else:
        user = User.get_or_none(User.id == id)
        updated_username = request.form.get("updated_username")
        updated_email = request.form.get("updated_email")
        user.username = updated_username
        user.email = updated_email
        if user.save():
            flash("Your profile has been updated good Sir!")
            return redirect(url_for('users.edit', id=id))
        else:
            flash("error, nothing has been changed")
            return redirect(url_for('users.edit', id=id))


@users_blueprint.route('/upload', methods=["POST"])
def upload():
    if not 'profile_image' in request.files:
        flash('where is your picture')
        return redirect(url_for('users.edit', id=current_user.id))
    file = request.files.get('profile_image')
    if file:
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)
        upload_profile_img = User.update(
            profile_image=file.filename).where(User.id == current_user.id)
        if upload_profile_img.execute():
            flash('awesome possum successfully uploaded picture')
            return redirect(url_for('users.edit', id=current_user.id))
        else:
            flash('alamak didnt work la cha!')
            return redirect(url_for('users.edit', id=current_user.id))
    else:
        return redirect(url_for('users.edit', id=current_user.id))
