from .base_model import BaseModel
import peewee as pw
import re
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
from config import S3_LINK
from flask import flash


class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)
    profile_image = pw.CharField(null=True, default=None)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)

        if duplicate_username and not duplicate_username.id == self.id:
            self.errors.append('Username not unique, you siham!')

        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_email and not duplicate_email.id == self.id:
            self.errors.append('Email not unique la MCH')

    @hybrid_property
    def profile_image_url(self):
        if self.profile_image:
            return f"{S3_LINK}/{self.profile_image}"
        else:
            return flash('no picture for shits', 'warning')
