from hashlib import sha256
from server import database


class User(database.DynamicDocument):
    full_name = database.StringField(max_length=32, required=True)
    email = database.StringField(max_length=64, required=True)
    password = database.StringField(max_length=64, required=True)

    @staticmethod
    def get_password(password):
        return sha256(password.encode()).hexdigest()