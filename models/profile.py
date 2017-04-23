from server import database


class Profile(database.DynamicDocument):
    vk = database.ListField(default=[])
    facebook = database.ListField(default=[])
    instagram = database.ListField(default=[])
    twitter = database.ListField(default=[])
    skype = database.ListField(default=[])
    email = database.ListField(default=[])
    phone = database.ListField(default=[])

    meta = {
        'collection': 'profile'
    }
