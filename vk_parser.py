import time

import vk

session = vk.Session()
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
