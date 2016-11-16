# -*- coding:utf-8 -*-

from flask import blueprints

auth = Blueprint('auth', __name__)

from . import views