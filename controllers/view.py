from flask import render_template, session, request, redirect
from server import app


def index():
    # for unlogined users - view landing page
    # for logined users - view manual
    return render_template('index.html')


def dashboard():
    pass


def task():
    pass


def create_task():
    pass