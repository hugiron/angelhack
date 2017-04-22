from flask import render_template, session, request, redirect
from server import app
from utils import finder
import json
from models.profile import Profile
from mongoengine import Q


def get_task():
    pass


def create_task():
    pass


def get_task_by_id():
    pass


def get_dashboard():
    pass


def get_dashboard_from_user():
    pass


def get_dashboard_from_text():
    pass


def find():
    network = request.args['network']
    user_id = int(request.args['user_id'])
    result = json.dumps(finder.find_network(network, user_id))
    print(result)
    return result
