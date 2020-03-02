from .base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        if duplicate_username and not duplicate_username.id == self.id:
            self.errors.append('Username not unique, you siham!')
        duplicate__email = User.get_or_none(User.email == self.email)
        if duplicate_email and not duplicate_email.id == self.id:
            self.errors.append('Email not unique la MCH')
