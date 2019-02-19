from flask import Blueprint, request, abort
from google.appengine.api import users
import json
import logging

import src.requests as req
from .blueprint_utils import flask_construct_response


""" Loader Blueprint """
LOAD_API_BLUEPRINT = Blueprint(u'load_api', __name__)

@LOAD_API_BLUEPRINT.route(u'/', methods=[u'GET'])
def list_loader():
    """
    API LIST Loader
    :return: Flask Response
    """
    items = req.list_load()
    return flask_construct_response({u'items': items})


@LOAD_API_BLUEPRINT.route(u'/add', methods=[u'POST'])
def add_loader():
    """
    API ADD Loader
    :return: Flask Response
    """
    pass
