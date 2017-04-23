import json
import string
import random
import itertools
import requests as rqst
from bs4 import BeautifulSoup


MEDIA_LINK = 'https://www.instagram.com/p/{{code}}'
ACCOUNT_JSON_INFO_BY_ID = "ig_user({{userId}}){id,username,external_url,full_name,profile_pic_url,biography," \
                          "followed_by{count},follows{count},media{count},is_private,is_verified}"
ACCOUNT_MEDIAS = "https://www.instagram.com/{{username}}/media?max_id={{maxId}}"
INSTAGRAM_QUERY_URL = "https://www.instagram.com/query/"
INSTAGRAM_URL = "https://www.instagram.com/"

TYPE_IMAGE = "image"
TYPE_VIDEO = "video"


class InstagramException(Exception):
    def __init__(self, message=''):
        self.message = message


class Account:
    def __init__(self):
        pass

    @staticmethod
    def empty():
        account = Account()
        account.id = None
        account.username = None
        account.follows_count = 0
        account.followed_by_count = 0
        account.media_count = 0
        account.profile_pic_url = None
        account.biography = ''
        account.full_name = ''
        account.is_private = False
        account.external_url = ''
        account.is_verified = False
        return account

    @staticmethod
    def create_from_account_page(response):
        account = Account()
        if type(response) == dict:
            data = response
        else:
            data = json.loads(response)
        account.id = data.get('id')
        account.username = data.get('username')
        account.follows_count = None if not data.get('follows') else  data.get('follows').get('count')
        account.followed_by_count = None if not data.get('followed_by') else data.get('followed_by').get('count')
        account.media_count = None if not data.get('media') else data.get('media').get('count')
        account.profile_pic_url = data.get('profile_pic_url')
        account.biography = data.get('biography')
        account.full_name = data.get('full_name')
        account.is_private = data.get('is_private')
        account.external_url = data.get('external_url')
        account.is_verified = data.get('is_verified')
        return account

    @staticmethod
    def create_from_media_page(response):
        account = Account()
        if type(response) == dict:
            data = response
        else:
            data = json.loads(response)
        account.id = data.get('id')
        account.username = data.get('username')
        account.profile_pic_url = data.get('profile_pic_url')
        account.full_name = data.get('full_name')
        account.is_private = data.get('is_private')
        return account


class Media:
    def __init__(self):
        pass

    @staticmethod
    def empty():
        media = Media()
        media.id = None
        media.type = TYPE_IMAGE
        media.created_time = 0
        media.code = ''
        media.link = '{0}p/{1}'.format(INSTAGRAM_URL, media.code)
        media.image_standard_resolution_url = ''
        media.caption = ''
        media.owner = Account.empty()
        return media

    @staticmethod
    def create_from_api(response):
        media = Media()
        if type(response) == dict:
            data = response
        else:
            data = json.loads(response)
        media.id = data.get('id')
        media.created_time = int(data.get('created_time'))
        media.type = data.get('type')
        media.link = data.get('link')
        media.code = data.get('code')
        if data.get('caption'):
            media.caption = data.get('caption').get('text')
        media.image_low_resolution_url = data.get('images').get('low_resolution').get('url')
        media.image_thumbnail_url = data.get('images').get('thumbnail').get('url')
        media.image_standard_resolution_url = data.get('images').get('standard_resolution').get('url')
        if media.type == TYPE_VIDEO:
            media.video_low_resolution_url = data.get('videos').get('low_resolution').get('url')
            media.video_standard_resolution_url = data.get('videos').get('standard_resolution').get('url')
            media.video_low_bandwidth_url = data.get('videos').get('low_bandwidth').get('url')
        return media

    @staticmethod
    def create_from_media_page(response):
        media = Media()
        if type(response) == dict:
            data = response
        else:
            data = json.loads(response)
        media.id = data.get('id')
        media.type = TYPE_IMAGE
        if data.get('is_video'):
            media.type = TYPE_VIDEO
            media.video_standard_resolution_url = data.get('video_url')
        media.created_time = int(data.get('date'))
        media.code = data.get('code')
        media.link = '{0}p/{1}'.format(INSTAGRAM_URL, media.code)
        media.image_standard_resolution_url = data.get('display_src')
        if data.get('caption'):
            media.caption = data.get('caption')
        media.owner = Account.create_from_media_page(data.get('owner'))
        return media

    @staticmethod
    def create_from_tag_page(response):
        media = Media()
        if type(response) == dict:
            data = response
        else:
            data = json.loads(response)
        media.code = data.get('code')
        media.link = get_media_page_link_by_code(code=media.code)
        media.comments_count = data.get('comments').get('count')
        media.likes_count = data.get('likes').get('count')
        media.owner_id = data.get('owner').get('id')
        if data.get('caption'):
            media.caption = data.get('caption')
        media.created_time = int(data.get('date'))
        media.image_thumbnail_url = data.get('thumbnail_src')
        media.image_standard_resolution_url = data.get('display_src')
        media.type = TYPE_IMAGE
        if data.get('is_video'):
            media.type = TYPE_VIDEO
            media.video_views = data.get('video_views')
        media.id = data.get('id')
        return media


def get_account_by_id(id):
    try:
        response = get_api_request(get_account_json_info_link_by_account_id(user_id=id))
        return Account.create_from_account_page(response=response.text)
    except Exception:
        return Account.empty()


def get_account_json_info_link_by_account_id(user_id):
    return ACCOUNT_JSON_INFO_BY_ID.replace("{{userId}}", str(user_id))


def get_media_page_link_by_code(code):
    return MEDIA_LINK.replace('{{code}}', code)


def get_account_medias_json_link(username, max_id):
    if not max_id:
        max_id = ''
    return ACCOUNT_MEDIAS.replace("{{username}}", username).replace("{{maxId}}", str(max_id))


def get_medias(username, count):
    medias = []
    try:
        index = 0
        max_id = ''
        is_more_available = True
        while index < count and is_more_available:
            response = rqst.get(get_account_medias_json_link(username=username, max_id=max_id))
            if response.status_code != 200:
                raise InstagramException('Response code is not equal 200. Something went wrong. Please report issue.')
            data = json.loads(response.text)
            if not data.get('items'):
                return medias
            for item in data.get('items'):
                if index == count:
                    return medias
                index += 1
                media = Media.create_from_api(item)
                medias.append(media)
                max_id = media.id
            is_more_available = data.get('more_available')
        return medias
    except Exception:
        return medias


def generate_random_string(size, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_api_request(params):
    csrf = generate_random_string(10)
    form = {'q': params}
    headers = {
        'Cookie': 'csrftoken=%s;' % csrf,
        'X-Csrftoken': csrf,
        'Referer': 'https://www.instagram.com/'
    }
    return rqst.post(
        url=INSTAGRAM_QUERY_URL,
        data=form,
        headers=headers
    )


def get_user_relationships(user_id):
    try:
        max_analyze_media_count = 100
        user = get_account_by_id(user_id)
        return list(set(itertools.chain(*list(map(lambda x: get_likes_and_comments_authors(x.code),
                                         get_medias(user.username, max_analyze_media_count))))))
    except:
        return []


def get_likes_and_comments_authors(code):
    result = list()
    try:
        request = rqst.get(get_media_page_link_by_code(code)).text
        parser = BeautifulSoup(request, 'html.parser')
        script = None
        for item in parser.findAll('script', attrs={'type': 'text/javascript'}):
            if item.text.strip().startswith('window._sharedData'):
                script = item.text.strip()
        if not script:
            return result
        data = json.loads(script[21:len(script) - 1])
        for item in data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_comment']['edges']:
            result.append(int(item['node']['owner']['id']))
        for item in data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_preview_like']['edges']:
            result.append(int(item['node']['id']))
    except:
        pass
    return result
