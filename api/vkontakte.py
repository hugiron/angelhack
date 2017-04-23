import vk


session = vk.Session()
api = vk.API(session)


def get_user_relationships(user_id):
    try:
        return api.friends.get(user_id=user_id)
    except:
        return []
