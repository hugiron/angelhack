from server import database


class Profile(database.DynamicDocument):
    vk = database.ListField(int, default=[])
    facebook = database.ListField(int, default=[])
    instagram = database.ListField(int, default=[])
    twitter = database.ListField(int, default=[])
    skype = database.ListField(str, default=[])
    email = database.ListField(str, default=[])
    phone = database.ListField(str, default=[])

    meta = {
        'collection': 'profile'
    }
