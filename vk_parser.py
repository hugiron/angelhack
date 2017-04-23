import datetime
import time

import vk
from dateutil.parser import parse

token = '6a757b028f97aff9dce19e3fc55d52daa06ad05aba65c0d1cb7b605b538cfd04466cfbba01a8bc496d3c7'
session = vk.Session(access_token=token)
vkapi = vk.API(session, v='5.63')


def get_group_members(group):
    members = vkapi.groups.getMembers(group_id=group, count=1)
    count = members['count']

    res = set(members['items'])
    last = 1

    while len(res) < count:
        while True:
            try:
                members = vkapi.execute.get_members(group=group, offset=last)
                time.sleep(1)
            except:
                time.sleep(3)
                pass
            break

        for x in members:
            res.add(x)

        last += len(members)

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

    count = posts["count"]

    res = [posts["items"][0]["text"]]

    try:
        res.append(posts["items"][0]["copy_history"][0]["text"])
    except:
        pass

    last = 1

    while len(res) < count:
        while True:
            try:
                posts = vkapi.wall.get(owner_id=user, offset=last)
                time.sleep(1 / 3)
            except:
                time.sleep(1)
                pass
            break

        for x in posts["items"]:
            res.append(x['text'])
            try:
                res.append(x['copy_history'][0]['text'])
            except:
                pass

        last += len(posts["items"])

    res = map(lambda x: x.strip(), res)

    return list(filter(lambda x: x != '', res))


def get_posts_within_area(query='иннополис', latitude='55.752874', longitude='48.743440'):
    resp = vkapi.newsfeed.search(q=query, latitude=latitude, longitude=longitude, count=200)
    posts = map(lambda x: x["text"].strip(), resp["items"])
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

        city = resp["city"]["title"]

        age = (datetime.datetime.now() - parse(resp["bdate"])).days // 365

        if age <= 0:
            age = ''

        vk_id = resp["id"]

        return {"vk_id": vk_id, "name": name, "sex": sex, "age": age, "city": city}
    except:
        return {"vk_id": user}
