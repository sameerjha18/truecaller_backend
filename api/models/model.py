from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, name, email, number, password):
        self.full_name = name
        self.email = email
        self.mobile_number = number
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

class BlockedNumber(db.Model):
    block_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reported_number = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, user_id, reported_number):
        self.user_id = user_id
        self.reported_number = reported_number