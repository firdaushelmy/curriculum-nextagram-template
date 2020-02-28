from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)
