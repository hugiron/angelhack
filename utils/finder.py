from keras.models import load_model
from mongoengine import Q
from models.profile import Profile
import api.instagram as instagram
import api.vkontakte as vkontakte
import api.twitter as twitter
from server import database
from subprocess import run, PIPE
from concurrent.futures import ThreadPoolExecutor
import numpy as np


handler = {
    'vk': vkontakte.get_user_relationships,
    'instagram': instagram.get_user_relationships,
    'twitter': twitter.get_user_relationships
}


model = load_model('network')


def find_network(network, user_id):
    result = {network: user_id}
    friends = handler[network](user_id)
    if network == 'vk':
        query = Q(vk__in=friends)
    elif network == 'instagram':
        query = Q(instagram__in=friends)
    elif network == 'twitter':
        query = Q(twitter__in=friends)
    else:
        return result
    data = {
        'vk': list(),
        'instagram': list(),
        'twitter': list()
    }
    for profile in Profile.objects(query):
        if network != 'vk' and profile.vk:
            for id in profile.vk:
                data['vk'].append(id)
        if network != 'instagram' and profile.instagram:
            for id in profile.instagram:
                data['instagram'].append(id)
        if network != 'twitter' and profile.twitter:
            for id in profile.twitter:
                data['twitter'].append(id)
    print("Profiles from database is finded") # DEBUG
    friends = {
        'vk': list(),
        'instagram': list(),
        'twitter': list()
    }
    with ThreadPoolExecutor(max_workers=12) as executor:
        for key in data:
            for item in executor.map(lambda x: handler[key](x), data[key]):
                for uid in item:
                    friends[key].append(uid)
            print("Parsing complete " + key)
    print("Friend list is generated") # DEBUG
    temp = {
        'vk': list(),
        'instagram': list(),
        'twitter': list()
    }
    for key in data:
        for id in data[key]:
            response = run(['dotnet', 'trainer/Bindex.Trainer.dll', network, str(user_id), key, str(id)],
                           stdout=PIPE, stderr=PIPE, universal_newlines=True)
            #try:
            vector = [float(item) for item in response.stdout.strip().split(' ')]
            factor = model.predict(np.array([vector]))[0][0]
            if factor >= 0.5:
                temp[key].append((id, factor))
            #except:
                #pass
    print("Neural network is used") # DEBUG
    for key in temp:
        if not temp[key]:
            continue
        result[key] = int(max(temp[key], key=lambda x: x[1])[0])
    print("Profiles from other networks is finded") # DEBUG
    return result
