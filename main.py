# coding: utf-8
from flask import Flask

from config import CONFIG
from src.commons.utils import init_logger
from src.blueprint import (LOAD_API_BLUEPRINT)
from src.blueprint.blueprint_utils import flask_constructor_error

import src.requests as req

logging_config = CONFIG[u"logging"]
init_logger(logging_config[u'pattern'], logging_config[u'pattern_debug'], logging_config[u"level"])


# create flask server
APP = Flask(__name__)
APP.debug = CONFIG[u"app"][u"debug"]
APP.register_blueprint(LOAD_API_BLUEPRINT, url_prefix=u'/api')


@APP.errorhandler(404)
def page_not_found(e):
    return flask_constructor_error(u"Not Found", 404, 404)

if __name__ == u"__main__":
    APP.run(threaded=True, port=5000, debug=True)