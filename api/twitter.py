import re
import requests as rqst
from bs4 import BeautifulSoup


username_regex = re.compile("id=\"twitter-([^\"]+)\"")
user_id_regex = re.compile("data-user-id=\"(\\d+)\"")


def get_user_id_by_username(username):
    response = rqst.get('https://twitter.com/' + username).text
    user_id = user_id_regex.findall(response)
    return int(user_id[0]) if user_id else None


def get_username_by_id(user_id):
    response = rqst.get('https://twitter.com/intent/user?user_id=' + str(user_id)).text
    username = username_regex.findall(response)
    return username[0] if username else None


def get_user_relationships(user_id):
    result = list()
    username = get_username_by_id(user_id)
    if not username:
        return result
    next_cursor = "/" + username + "/following"
    while next_cursor:
        response = rqst.get("https://mobile.twitter.com" + next_cursor).text
        parser = BeautifulSoup(response, 'html.parser')
        next_cursor = parser.find('div', attrs={'class': 'w-button-more'}).find('a').get('href')
        for username in parser.find_all('span', attrs={'class': 'username'}):
            result.append(get_user_id_by_username(username.text[1:]))
    return list(set(result))
