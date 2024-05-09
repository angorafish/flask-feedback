from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    def __init__(self, username, password, email, first_name, last_name):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)