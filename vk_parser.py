import datetime
import time

import vk
from dateutil.parser import parse

token = '74701fb474701fb474701fb494742b9f2b7747074701fb42c8b34241d33607df85a6114'

session = vk.Session(access_token=token)
vkapi = vk.API(session)


def get_group_members(group):
    members = vkapi.groups.getMembers(group_id=group, count=1)

    count = members['count']

    res = set(members['users'])
    last = 1

    while len(res) < count:
        while True:
            try:
                members = vkapi.groups.getMembers(group_id=group, offset=last)
            except:
                time.sleep(1)
                pass
            break

        for x in members['users']:
            res.add(x)

        last += len(members['users'])

    return res


def monitor_group(group):
    members = get_group_members(group)
    members_last = members

    while True:
        members = get_group_members(group)

        added = members - members_last
        deleted = members_last - members

        members_last = members
        yield {'added': added, 'deleted': deleted}


def get_user_posts(user):
    try:
        posts = vkapi.wall.get(owner_id=user, count=1)
    except:
        return []

    count = posts[0]

    res = [posts[1]['text']]
    last = 1

    while len(res) < count:
        while True:
            try:
                posts = vkapi.wall.get(owner_id=user, offset=last)
            except:
                time.sleep(1)
                pass
            break

        for x in posts[1:]:
            res.append(x['text'])

        last += len(posts[1:])

    res = map(lambda x: x.strip(), res)

    return list(filter(lambda x: x != '', res))


def get_posts_within_area(query='иннополис', latitude='55.752874', longitude='48.743440'):
    resp = vkapi.newsfeed.search(q=query, latitude=latitude, longitude=longitude, count=200)
    posts = map(lambda x: x["text"].strip(), resp[1:])
    return list(filter(lambda x: x != '', posts))


def get_user_data(user):
    try:
        resp = vkapi.users.get(user_ids=[user], fields=["city", "sex", "bdate"], name_case="Nom")[0]

        name = resp["first_name"] + " " + resp["last_name"]
        sex = resp["sex"]

        if sex == 0:
            sex = ''
        if sex == 1:
            sex = 'жен.'
        if sex == 2:
            sex = 'муж.'

        city_id = resp["city"]

        city = vkapi.database.getCitiesById(city_ids=[city_id])[0]["name"]

        age = (datetime.datetime.now() - parse(resp["bdate"])).days // 365

        if age <= 0:
            age = ''

        vk_id = resp["uid"]

        return {"vk_id": vk_id, "name": name, "sex": sex, "age": age, "city": city}
    except:
        return {"vk_id": user}
