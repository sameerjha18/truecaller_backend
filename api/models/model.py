from mongoengine import Document, StringField, EmailField, IntField, ReferenceField,DateTimeField
from datetime import datetime


class User(Document):
    full_name = StringField(max_length=50, required=True)
    email = EmailField(max_length=50, required=False)
    password = StringField(max_length=100, required=True)
    mobile_number = IntField(unique=True, required=True)


class BlockedNumber(Document):
    user_id = ReferenceField(User, required=True)
    reported_number = IntField(required=True)
    timestamp = DateTimeField(default=datetime.now)
