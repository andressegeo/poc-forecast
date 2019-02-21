# coding: utf-8
# !/usr/bin/python

import logging
import time
from datetime import datetime

from flask import abort

from config import CONFIG

def list_load():
    items = []
    try:
        pass
    except Exception as e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
    return items
