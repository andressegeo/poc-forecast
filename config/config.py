# coding: utf-8
"""
Configuration file.
"""
import logging

CONFIG = {
    u"db": {
        u"client": u"mongodb://andressen:namesgeo@namescluster-shard-00-00-y0phk.gcp.mongodb.net:27017,namescluster-shard-00-01-y0phk.gcp.mongodb.net:27017,namescluster-shard-00-02-y0phk.gcp.mongodb.net:27017/test?ssl=true&replicaSet=namesCluster-shard-0&authSource=admin&retryWrites=true",
        u"database": "poc_forecast",
        u"collection": [u'load', u'loadforecast', u'weather', u'weatherforecast']
    },
    u"logging": {
        u"level": logging.INFO,
        u"pattern": u'%(levelname)s - %(asctime)s : %(message)s',
        u"pattern_debug": u'[%(filename)15s::%(funcName)15s]-[l.%(lineno)3s] %(message)s'
    },
    u"app": {
        u"env": u"dev",
        u"debug": True
    }
}
